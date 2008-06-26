__author__ = 'Ping Chen'

import cgi
import wsgiref.handlers
import os
import re
import datetime
import calendar
import logging
import string

from xml.etree import ElementTree

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

from cpedia.pagination.GqlQueryPaginator import GqlQueryPaginator,GqlPage
from cpedia.pagination.paginator import InvalidPage,Paginator
from cpedia.util import translate

from model import Weblog,WeblogReactions
import authorized
import view
import config


# Functions to generate permalinks
def get_permalink(date,title):
     return str(date.year) + "/" + str(date.month) + "/" + get_friendly_url(title)

# Module methods to handle incoming data
def get_datetime(time_string):
    if time_string:
        return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime.now()

def get_friendly_url(title):
    return re.sub('-+', '-', re.sub('[^\w-]', '', re.sub('\s+', '-', title.strip())))

def u(s, encoding):
      if isinstance(s, unicode):
       return s
      else:
       return unicode(s, encoding)


#get the archive monthe list.
def getDatetimeList():
  weblog = Weblog.all().order('date').get()
  monthlist = []
  if weblog:
      startDate = weblog.date
      startYear = int(datetime.datetime.strftime(startDate,'%Y'))
      startMonth = int(datetime.datetime.strftime(startDate,'%m'))
      #endDate = int(datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d'))
      endDate =  datetime.datetime.now()
      endYear = int(datetime.datetime.strftime(endDate,'%Y'))
      endMonth = int(datetime.datetime.strftime(endDate,'%m'))
      for year in range(startYear,endYear+1):
          if year == startYear:
             if startYear == endYear:
               monthlist.extend(makeMonthList(year,startMonth,endMonth+1))
             else:
               monthlist.extend(makeMonthList(year,startMonth,12+1))
          else:
             if year ==endYear:
                monthlist.extend(makeMonthList(year,1,endMonth+1))
             else:
                monthlist.extend(makeMonthList(year,1,12+1))
  return monthlist

def makeMonthList(year,startMonth,endMonth):
     day = 1
     monthList = []
     for month in range(startMonth,endMonth):
         date = datetime.date(year,month,day)
         monthList.append(date)
     return monthList




class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    administrator = False
    useremail = ""
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Sign out'
      useremail = users.get_current_user().email()
      if users.is_current_user_admin():
         administrator = True
      else:
         if useremail == 'ping.chen@cpedia.com':
              administrator = True        
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Sign in'
    logoImages = ("logo1.gif","logo2.gif")
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'url': url,
      'url_linktext': url_linktext,
      'administrator': administrator,
      'logoImages': logoImages,
      'datetimeList': getDatetimeList(),
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    view.ViewPage(cache_time=0).render(self, template_name,values)
    #self.response.out.write(template.render(path, values, debug=config._DEBUG))


class NotFoundHandler(webapp.RequestHandler):
    def get(self):
        self.error(404)
        view.ViewPage(cache_time=36000).render(self)

class UnauthorizedHandler(webapp.RequestHandler):
    def get(self):
        self.error(403)
        view.ViewPage(cache_time=36000).render(self)
        
class MainPage(BaseRequestHandler):
  def get(self):
    pageStr = self.request.get('page')
    if pageStr:
        page = int(pageStr)
    else:
        page = 1;
    blogs_query = Weblog.all().order('-date')
    #blogs = blogs_query.fetch(5,(page-1)*5)
    try:
        obj_page  =  GqlQueryPaginator(blogs_query,page,config._NUM_PER_PAGE).page()
    except InvalidPage:
        self.redirect('/')

    recentReactions = WeblogReactions.all().order('-date').fetch(20)
    template_values = {
      'page':obj_page,
      'recentReactions':recentReactions,
      }
    self.generate('blog_main.html',template_values)


class AddBlog(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    template_values = {
      'action': "addBlog",
      }
    self.generate('blog_add.html',template_values)

  @authorized.role("admin")
  def post(self):
    title_review = self.request.get('title_input')
    content_review = self.request.get('text_input')

    preview = self.request.get('preview')
    submitted = self.request.get('submitted')

    user = users.get_current_user()

    template_values = {
      'title_review': title_review,
      'content_review': content_review,
      'preview': preview,
      'submitted': submitted,
      'action': "addBlog",
      }

    if preview == '1' and submitted !='1':
        self.generate('blog_add.html',template_values)
    else:
      if submitted =='1':
        blog = Weblog()
        blog.title = title_review
        blog.content = content_review
        blog.author = user
        blog.authorEmail = user.email()
        blog.put()
        self.redirect('/')

class AddBlogReaction(BaseRequestHandler):
  def post(self):
    title_review = self.request.get('title_input')
    content_review = self.request.get('text_input')

    blogId_ = self.request.get('blogId')
    blog= Weblog.get_by_id(int(blogId_))

    if(blog is None):
        self.redirect('/')
    blogReaction = WeblogReactions()
    blogReaction.weblog = blog
    blogReaction.user = self.request.get('name_input')
    blogReaction.content = self.request.get('text_input')
    user = users.get_current_user()
    clientIp = self.request.remote_addr  
    if not user:
      user  = users.User("Anonymous@"+clientIp)

    blogReaction.author = user
    blogReaction.authorEmail = user.email()
    blogReaction.userIp = clientIp 
    blogReaction.put()
    self.redirect('/viewBlog?blogId='+blogId_)


class EditBlog(BaseRequestHandler):
    @authorized.role("admin")
    def get(self):
        blogId_ = self.request.get('blogId')
        blog = Weblog.get_by_id(int(blogId_))
        template_values = {
        'blog': blog,
        'action': "editBlog",
        }
        self.generate('blog_add.html',template_values)

    @authorized.role("admin")
    def post(self):
        blogId_ = self.request.get('blogId')
        blog= Weblog.get_by_id(int(blogId_))

        if(blog is None):
            self.redirect('/')

        blog.title = self.request.get('title_input')
        blog.content = self.request.get('text_input')
        user = users.get_current_user()
        blog.lastModifiedDate = datetime.datetime.now()
        blog.lastModifiedBy = user
        blog.put()
        self.redirect('/viewBlog?blogId='+blogId_)

class DeleteBlog(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
      blogId_ = self.request.get('blogId')
      blog = Weblog.get_by_id(int(blogId_))
      template_values = {
      'blog': blog,
      'action': "deleteBlog",
      }
      self.generate('blog_delete.html',template_values)

  @authorized.role("admin")
  def post(self):
    blogId_ = self.request.get('blogId')
    blog= Weblog.get_by_id(int(blogId_))
    if(blog is not None):
        blogReactions = blog.weblogreactions_set
        for reaction in blogReactions:
            reaction.delete()
        blog.delete()
    self.redirect('/')

class EditBlogReaction(BaseRequestHandler):
    @authorized.role("user")
    def get(self):
        reactionId_ = self.request.get('reactionId')
        blogReaction = WeblogReactions.get_by_id(int(reactionId_))
        template_values = {
        'blogReaction': blogReaction,
        'action': "editBlogReaction",
        }
        self.generate('blog_add.html',template_values)

    @authorized.role("user")
    def post(self):
        blogReactionId_ = self.request.get('blogReactionId')
        blogReaction= WeblogReactions.get_by_id(int(blogReactionId_))

        if(blogReaction is None):
            self.redirect('/')

        blogReaction.content = self.request.get('text_input')
        user = users.get_current_user()

        blogReaction.lastModifiedBy = user
        blogReaction.lastModifiedDate = datetime.datetime.now()
        blogReaction.put()
        self.redirect('/viewBlog?blogId='+str(blogReaction.weblog.key().id()))


class DeleteBlogReaction(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
      reactionId_ = self.request.get('reactionId')
      blogReaction = WeblogReactions.get_by_id(int(reactionId_))
      template_values = {
      'blogReaction': blogReaction,
      'action': "deleteBlogReaction",
      }
      self.generate('blog_delete.html',template_values)

  @authorized.role("admin")
  def post(self):
    blogReactionId_ = self.request.get('blogReactionId')
    blogReaction= WeblogReactions.get_by_id(int(blogReactionId_))

    if(blogReaction is not None):
        db.delete(blogReaction)
    self.redirect('/')


class ViewBlog(BaseRequestHandler):
  def get(self):
    blogId_ = self.request.get('blogId')
    blog= Weblog.get_by_id(int(blogId_))

    if(blog is None):
        self.redirect('/')
    permalink = ""
    if not blog.permalink:
          permalink =  get_permalink(blog.date,translate.translate('zh-CN','en', u(blog.title,'utf-8')))
          blog.permalink =  permalink.lower()
          blog.put()

    reactions = db.GqlQuery("select * from WeblogReactions where weblog =:1  order by date", blog) 
    template_values = {
      'blog': blog,
      'reactions': reactions,
      'permalink': permalink,
      }
    self.generate('blog_view.html',template_values)


class MonthHandler(BaseRequestHandler):
    def get(self, year, month):
        logging.debug("MonthHandler#get for year %s, month %s", year, month)
        pageStr = self.request.get('page')
        if pageStr:
            page = int(pageStr)
        else:
            page = 1;
        year_ =  string.atoi(year)
        month_ =  string.atoi(month)
        start_date = datetime.datetime(year_, month_, 1)
        end_date = datetime.datetime(year_, month_, calendar.monthrange(year_, month_)[1], 23, 59, 59)
        blogs_query = db.Query(Weblog).order('-date').filter('date >=', start_date).filter('date <=', end_date)
        try:
            obj_page  =  GqlQueryPaginator(blogs_query,page,config._NUM_PER_PAGE).page()
        except InvalidPage:
            self.redirect('/')

        recentReactions = WeblogReactions.all().order('-date').fetch(20)
        template_values = {
          'page':obj_page,
          'recentReactions':recentReactions,
          }
        self.generate('blog_main.html',template_values)

class ArticleHandler(BaseRequestHandler):
    def get(self, year, month, perm_stem):
        logging.debug("ArticleHandler#get for year %s, month %s, and perm_link %s", year, month, perm_stem)
        blog = db.Query(Weblog).filter('permalink =', year + '/' + month + '/' + perm_stem).get()
        if(blog is None):
            self.redirect('/')
        reactions = db.GqlQuery("select * from WeblogReactions where weblog =:1  order by date", blog)
        template_values = {
          'blog': blog,
          'reactions': reactions,
          }
        self.generate('blog_view.html',template_values)




#The method below just for blog data maintance.   
class DeleteAllBlog(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    user = users.get_current_user()
    weblogs = Weblog.all().fetch(1000)
    for blog in weblogs:
        blogReactions = blog.weblogreactions_set
        for reaction in blogReactions:
            reaction.delete()
        blog.delete()
    self.response.out.write("success!")

class DeleteAllBlogReaction(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    user = users.get_current_user()
    blogreactions = WeblogReactions.all().fetch(1000)
    for reaction in blogreactions:
        reaction.delete()         
    self.response.out.write("success!")

class LoadBlogBulk(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    user = users.get_current_user()
    file = self.request.get('file')
    root = ElementTree.parse(file+'.xml').getroot()
    for element in root.findall('weblog'):
        blog = Weblog()
        blog._weblogId = int(element.findtext('id'))
        blog.title = element.findtext('title')
        blog.content = element.findtext('text')
        blog.date = datetime.datetime.strptime(str(element.findtext('date')),'%Y%m%d%H%M')
        blog.author = user
        blog.authorEmail = user.email()
        blog.put()
    self.response.out.write("success!")

class LoadBlogReactionBulk(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    user = users.get_current_user()
    file = self.request.get('file')
    root = ElementTree.parse(file+'.xml').getroot()
    for element in root.findall('weblog_reactions'):
        blogreaction = WeblogReactions()
        weblogId =  int(element.findtext('weblog'))
        blog = Weblog.gql("where _weblogId =:1",weblogId).get()
        if blog:
            blogreaction.weblog = blog
            blogreaction._weblogReactionId = int(element.findtext('id'))
            blogreaction.user =  element.findtext('user')
            blogreaction.content = element.findtext('text')
            blogreaction.userIp = element.findtext('ip')
            blogreaction.date = datetime.datetime.strptime(str(element.findtext('date')),'%Y%m%d%H%M')
            blogreaction.put()
    self.response.out.write("success!")

class SetBlogPermalinks(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
    pageStr = self.request.get('page')
    if pageStr:
        page = int(pageStr)
    else:
        page = 1;
    blogs_query = Weblog.all().order('-date')
    blogs = blogs_query.fetch(20,(page-1)*20)
    for blog in blogs:
        if not blog.permalink:
            permalink =  get_permalink(blog.date,translate.translate('zh-CN','en', u(blog.title,'utf-8')))
            blog.permalink =  permalink.lower()

    self.response.out.write("set permalink success for page!"+page)



