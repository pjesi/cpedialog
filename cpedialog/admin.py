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

from model import Archive,Weblog,WeblogReactions,AuthSubStoredToken,Album,Menu
import authorized
import view
import config
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
    path = os.path.join(directory, os.path.join('templates', template_name))
    view.ViewPage(cache_time=0).render(self, template_name,values)


class MainPage(BaseRequestHandler):
  @authorized.role('admin')
  def get(self):
        cache_stats = memcache.get_stats()
        session_tokens = AuthSubStoredToken.all()
        albums = Album.all()
        pages = Weblog.all().filter('entrytype','page').order('-date')
        menu= Menu()
        menu.title = "toolbox"
        menu.permalink = "08/07/toolbox"
        menu.target = "_blank"
        menu.order = 2
        menu.valid = True
        #menu.put()
        menus = Menu.all().filter('valid',True).order('order')
        template_values = {
          'pages':pages,
          'menus':menus,
          'session_tokens':session_tokens,
          'albums':albums,
          'cache_stats':cache_stats,
          }
        self.generate('admin_main.html',template_values)

