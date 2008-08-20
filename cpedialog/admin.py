__author__ = 'Ping Chen'


import gdata.photos.service
import gdata.media
import gdata.geo
import atom

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

from model import Archive,Weblog,WeblogReactions,AuthSubStoredToken,Album,Menu,Images,Tag,Feeds
import authorized
import view
import util

import gdata.urlfetch
gdata.service.http_request_handler = gdata.urlfetch

class BaseRequestHandler(webapp.RequestHandler):
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    view.ViewPage(cache_time=0).render(self, template_name,values)


class MainPage(BaseRequestHandler):
  @authorized.role('admin')
  def get(self):
        cache_stats = memcache.get_stats()
        session_tokens = AuthSubStoredToken.all()
        pages = Weblog.all().filter('entrytype','page').order('-date')
        menus = Menu.all().order('order')
        template_values = {
          'pages':pages,
          'menus':menus,
          'session_tokens':session_tokens,
          'cache_stats':cache_stats,
          }
        self.generate('admin_main.html',template_values)

  @authorized.role('admin')
  def post(self):
        cpedialogs = CPediaLog().all().filter("default",True)
        if cpedialogs:
            cpedialog = cpedialogs.get()
        else:
            cpedialog = CPediaLog()
        cpedialog.title = self.request.get("title")
        cpedialog.author = self.request.get("author")
        cpedialog.email = self.request.get("email")
        cpedialog.root_url = self.request.get("root_url")
        cpedialog.logo_images_space = self.request.get("logo_images_space")
        cpedialog.num_post_per_page = int(self.request.get("num_post_per_page"))
        cpedialog.cache_time = int(self.request.get("cache_time"))
        if self.request.get("debug"):
            cpedialog.debug = True
        else:
            cpedialog.debug = False
        cpedialog.host_ip = self.request.remote_addr
        cpedialog.host_domain = self.request.remote_addr

        if self.request.get("recaptcha_enable"):
            cpedialog.recaptcha_enable = True
            cpedialog.recaptcha_public_key =  self.request.get("recaptcha_public_key")
            cpedialog.recaptcha_private_key =  self.request.get("recaptcha_private_key")
        else:
            cpedialog.recaptcha_enable = False
            
        if self.request.get("delicious_enable"):
            cpedialog.delicious_enable = True
            cpedialog.delicious_username =  self.request.get("delicious_username")
        else:
            cpedialog.delicious_enable = False

        if self.request.get("google_ajax_feed_enable"):
            cpedialog.google_ajax_feed_enable = True
            cpedialog.google_ajax_feed_title =  self.request.get("google_ajax_feed_title")
            cpedialog.google_ajax_feed_result_num = int(self.request.get("google_ajax_feed_result_num"))
        else:
            cpedialog.google_ajax_feed_enable = False

        cpedialog.put()

        cache_stats = memcache.get_stats()
        session_tokens = AuthSubStoredToken.all()
        pages = Weblog.all().filter('entrytype','page').order('-date')
        menus = Menu.all().order('order')
        feeds = Feeds.all().order('order')
        template_values = {
          'BLOG':cpedialog,
          'pages':pages,
          'menus':menus,
          'session_tokens':session_tokens,
          'cache_stats':cache_stats,
          }
        self.generate('admin_main.html',template_values)

        
class AdminMorePage(BaseRequestHandler):
  @authorized.role('admin')
  def get(self):
        albums = Album.all().order('order')
        feeds = Feeds.all().order('order')
        tags = Tag.all().order('-entrycount')
        archives = Archive.all().order('-date')
        template_values = {
          'albums':albums,
          'feeds':feeds,
          'tags':tags,
          'archives':archives,
          }
        self.generate('admin_more.html',template_values)

