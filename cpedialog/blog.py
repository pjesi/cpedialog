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
from google.appengine.api import memcache
from google.appengine.ext import search

from cpedia.pagination.GqlQueryPaginator import GqlQueryPaginator,GqlPage
from cpedia.pagination.paginator import InvalidPage,Paginator
from cpedia.util import translate

from model import Weblog,WeblogReactions
import authorized
import view
import config
import util


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
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Sign in'
    values = {
      'request': self.request,
      'user': users.GetCurrentUser(),
      'url': url,
      'url_linktext': url_linktext,
      'administrator': administrator,
      'logoImages': util.getLogoImagesList(),
      'datetimeList': util.getDatetimeList(),
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    view.ViewPage(cache_time=0).render(self, template_name,values)


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

    #get blog pagination from cache.
    obj_page = util.getBlogPagination(page)
    if obj_page is None:
        self.redirect('/')

    recentReactions = util.getRecentReactions()
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
    preview = self.request.get('preview')
    submitted = self.request.get('submitted')
    user = users.get_current_user()

    blog = Weblog()
    blog.title = self.request.get('title_input')
    blog.content = self.request.get('text_input')
    blog.author = user
    blog.authorEmail = user.email()
    blog.tags_commas = self.request.get('tags')
    template_values = {
      'blog': blog,
      'preview': preview,
      'submitted': submitted,
      'action': "addBlog",
      }
    if preview == '1' and submitted !='1':
        self.generate('blog_add.html',template_values)
    else:
      if submitted =='1':
        try:
            permalink =  util.get_permalink(blog.date,translate.translate('zh-CN','en', util.u(blog.title,'utf-8')))
            if not permalink:
                raise Exception
        except Exception:
            #todo: notice user that the permalink genereted error.
            template_values.update({'error':'Generate permanent link for blog error, please retry it.'})
            self.generate('blog_add.html',template_values)
            return
        #check the permalink duplication problem.
        maxpermalinkBlog = db.GqlQuery("select * from Weblog where permalink >= :1 and permalink < :2 order by permalink desc",permalink, permalink+u"\xEF\xBF\xBD").get()
        if maxpermalinkBlog is not None:
            permalink = maxpermalinkBlog.permalink+"1"
        blog.permalink =  permalink
        blog.put()
        util.flushBlogMonthCache(blog)
        util.flushBlogPagesCache()
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
    blogReaction.content = self.request.get('text_input')
    blogReaction.authorWebsite = self.request.get('website')
    
    user = users.get_current_user()
    clientIp = self.request.remote_addr

    if user is not None:
        blogReaction.author = user
        blogReaction.authorEmail = str(user.email)
        blogReaction.user = str(user.nickname)
    else:
        blogReaction.authorEmail = self.request.get('mail')
        blogReaction.user = self.request.get('name_input')
    blogReaction.userIp = clientIp
    blogReaction.put()
    util.flushRecentReactions()
    self.redirect('/'+blog.permalink)


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
        util.flushBlogMonthCache(blog)
        util.flushBlogPagesCache()
        self.redirect('/'+blog.permalink)

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
        util.flushBlogMonthCache(blog)
        util.flushBlogPagesCache()
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
        blogReaction.authorWebsite = self.request.get('website')
        user = users.get_current_user()
        if user is not None:
            blogReaction.lastModifiedBy = user
        else:
            blogReaction.authorEmail = self.request.get('mail')
            blogReaction.user = self.request.get('name_input')

        blogReaction.lastModifiedDate = datetime.datetime.now()
        blogReaction.put()
        self.redirect('/'+blogReaction.weblog.permalink)


class DeleteBlogReaction(BaseRequestHandler):
  @authorized.role("admin")
  def get(self):
      reactionId_ = self.request.get('reactionId')
      blogReaction = WeblogReactions.get_by_id(int(reactionId_))
      template_values = {
      'reaction': blogReaction,
      'action': "deleteBlogReaction",
      }
      self.generate('blog_delete.html',template_values)

  @authorized.role("admin")
  def post(self):
    blogReactionId_ = self.request.get('blogReactionId')
    blogReaction= WeblogReactions.get_by_id(int(blogReactionId_))

    if(blogReaction is not None):
        db.delete(blogReaction)
        util.flushRecentReactions()
    self.redirect('/'+blogReaction.weblog.permalink)


class ViewBlog(BaseRequestHandler):
  def get(self):
    blogId_ = self.request.get('blogId')
    blog= Weblog.get_by_id(int(blogId_))

    if(blog is None):
        self.redirect('/')
    permalink = ""
    if not blog.permalink:
          permalink =  util.get_permalink(blog.date,translate.translate('zh-CN','en', util.u(blog.title,'utf-8')))
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
        year_ =  string.atoi(year)
        month_ =  string.atoi(month)

        #get blogs in month from cache.
        blogs = util.getMonthBlog(year_,month_)

        recentReactions = util.getRecentReactions()
        template_values = {
          'blogs':blogs,
          'recentReactions':recentReactions,
          }
        self.generate('blog_main_month.html',template_values)


class ArticleHandler(BaseRequestHandler):
    def get(self, year, month, perm_stem):
        blog = db.Query(Weblog).filter('permalink =', year + '/' + month + '/' + perm_stem).get()
        if(blog is None):
            self.redirect('/')
        reactions = db.GqlQuery("select * from WeblogReactions where weblog =:1  order by date", blog)
        template_values = {
          'blog': blog,
          'reactions': reactions,
          }
        self.generate('blog_view.html',template_values)

class SearchHandler(BaseRequestHandler):
    def get(self):
        pageStr = self.request.get('page')
        if pageStr:
            page = int(pageStr)
        else:
            page = 1;
        search_term = self.request.get("q")
        query = search.SearchableQuery('Weblog')
        query.Search(search_term)
        result = query.Run()
        try:
            obj_page  =  Paginator(result,config._NUM_PER_PAGE)
        except InvalidPage:
            self.redirect('/')

        recentReactions = util.getRecentReactions()
        template_values = {
          'page':obj_page,
          'recentReactions':recentReactions,
          }
        self.generate('blog_main.html',template_values)


class TagHandler(BaseRequestHandler):
    def get(self, encoded_tag):
        tag =  re.sub('(%25|%)(\d\d)', lambda cmatch: chr(string.atoi(cmatch.group(2), 16)), encoded_tag)   # No urllib.unquote in AppEngine?         
        blogs_query = db.Query(Weblog).filter('tags =', tag).order('-date')
        blogs = blogs_query.fetch(1000)
        recentReactions = util.getRecentReactions()
        template_values = {
          'blogs':blogs,
          'tag':tag,
          'recentReactions':recentReactions,
          }
        self.generate('tag.html',template_values)
        

        
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