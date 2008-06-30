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

import authorized
import view
import config
import util

import gdata.urlfetch
gdata.service.http_request_handler = gdata.urlfetch



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


class MainPage(BaseRequestHandler):
  def get(self):
    username =config.album['username']
    gd_client = gdata.photos.service.PhotosService()
    feed = gd_client.GetUserFeed(user=username)

    template_values = {
      'username':username,
      'albums':feed.entry,
       }
    self.generate('album_main.html',template_values)


class AlbumHandler(BaseRequestHandler):
    def get(self, username, album_name):
        logging.debug("AlbumHandler#get for username %s and album_name %s", username, album_name)
        gd_client = gdata.photos.service.PhotosService()
        feed = gd_client.GetFeed(
            '/data/feed/api/user/%s/album/%s?kind=photo' % (
                username, album_name))
        template_values = {
          'photos': feed.entry,
          'username':username,
          'album_name':album_name,
          }
        self.generate('album_view.html',template_values)


class PhotoHandler(BaseRequestHandler):
    def get(self, username, album_name, photoId):
        logging.debug("AlbumHandler#get for username %s, album_name %s and photoId %s", username, album_name, photoId)
        gd_client = gdata.photos.service.PhotosService()
        feed = gd_client.GetFeed(
            '/data/feed/api/user/%s/album/%s?kind=photo' % (
                username, album_name))
        template_values = {
          'photos': feed.entry,
          'username':username,
          'album_name':album_name,
          }
        self.generate('album_photo_view.html',template_values)
