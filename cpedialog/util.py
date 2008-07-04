__author__ = 'Ping Chen'

import os
import re
import datetime
import calendar
import logging
import string
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache

from cpedia.pagination.GqlQueryPaginator import GqlQueryPaginator,GqlPage
from cpedia.pagination.paginator import InvalidPage,Paginator

from model import Weblog,WeblogReactions
import config


# Functions to generate permalinks
def get_permalink(date,title):
    return str(date.year) + "/" + str(datetime.datetime.strftime(date,'%m')) + "/" + get_friendly_url(title)

# Module methods to handle incoming data
def get_datetime(time_string):
    if time_string:
        return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime.now()

def get_friendly_url(title):
    return re.sub('-+', '-', re.sub('[^\w-]', '', re.sub('\s+', '-', removepunctuation(title).strip()))).lower()

def removepunctuation(str):
    punctuation = re.compile(r'[.?!,":;]')
    str = punctuation.sub("", str)
    return str

def u(s, encoding):
    if isinstance(s, unicode):
        return s
    else:
        return unicode(s, encoding)


#get the archive monthe list. Cached.
def getDatetimeList():
    key_ = "blog_datetimeList_key"
    try:
        monthlist = memcache.get(key_)
    except Exception:
        monthlist = None
    if monthlist is None:
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
        memcache.add(key=key_, value=monthlist, time=3600)
    else:
        logging.debug("getDatetimeList from cache. ")
    return monthlist

def makeMonthList(year,startMonth,endMonth):
    day = 1
    monthList = []
    for month in range(startMonth,endMonth):
        date = datetime.date(year,month,day)
        monthList.append(date)
    return monthList


#get log images list. Cached.
def getLogoImagesList():
    key_ = "blog_logoImagesList_key"
    try:
        logoImagesList = memcache.get(key_)
    except Exception:
        logoImagesList = None
    if logoImagesList is None:
        logoImagesList = []
        directory = os.path.dirname(__file__)
        path = os.path.normpath(os.path.join(directory, 'img/logo/'))
        files = os.listdir(path)
        for file in files:
            (shortname, extension) = os.path.splitext(file)
            if extension.lower() == ".gif":
                logoImagesList.append(file)
        memcache.add(key=key_, value=logoImagesList, time=3600)
    else:
        logging.debug("getLogoImagesList from cache. ")
    return logoImagesList

#get recent comments. Cached.
def getRecentReactions():
    key_ = "blog_recentReactions_key"
    try:
        recentReactions = memcache.get(key_)
    except Exception:
        recentReactions = None
    if recentReactions is None:
        recentReactions = WeblogReactions.all().order('-date').fetch(20)
        memcache.add(key=key_, value=recentReactions, time=3600)
    else:
        logging.debug("getRecentReactions from cache. ")

    return recentReactions


#get blog pagination. Cached.
def getBlogPagination(page):
    key_ = "blog_pages_key"
    try:
        obj_pages = memcache.get(key_)
    except Exception:
        obj_pages = None
    if obj_pages is None or page not in obj_pages:
        blogs_query = Weblog.all().order('-date')
        try:
            obj_page  =  GqlQueryPaginator(blogs_query,page,config._NUM_PER_PAGE).page()
            if obj_pages is None:
                obj_pages = {}
            obj_pages[page] = obj_page
            memcache.add(key=key_, value=obj_pages, time=3600)
        except InvalidPage:
            return None
    else:
        logging.debug("getBlogPagination from cache. ")

    return obj_pages[page]

#get blogs in some month. Cached.
def getMonthBlog(year,month):
    key_= "blog_year_month_"+str(year)+"_"+str(month)+"_key"
    try:
        blogs = memcache.get(key_)
    except Exception:
        blogs = None    
    if blogs is None:
        start_date = datetime.datetime(year, month, 1)
        end_date = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        blogs_query = db.Query(Weblog).order('-date').filter('date >=', start_date).filter('date <=', end_date)
        blogs = blogs_query.fetch(1000)
        memcache.add(key=key_, value=blogs, time=3600)
    else:
        logging.debug("getMonthBlog from cache. ")
    return blogs


#flush recent comments.
def flushRecentReactions():
    memcache.delete("blog_recentReactions_key")

#flush blog pagination.
def flushBlogPagesCache():
    memcache.delete("blog_pages_key")

#flush month-cached blog.
def flushBlogMonthCache(blog):
    if blog.date is None:
        blog.date = datetime.datetime.now()
    year_ =  blog.date.year
    month_ =  blog.date.month
    key= "blog_year_month_"+str(year_)+"_"+str(month_)+"_key"
    memcache.delete(key)
        