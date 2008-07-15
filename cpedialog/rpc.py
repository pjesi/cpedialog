__author__ = 'Ping Chen'


import os
import logging
import datetime
import simplejson
import wsgiref.handlers

from google.appengine.api import datastore
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import memcache

from model import Archive,Weblog,WeblogReactions,AuthSubStoredToken,Album,CPediaLog

import authorized

# This handler allows the functions defined in the RPCHandler class to
# be called automatically by remote code.
class RPCHandler(webapp.RequestHandler):
  def get(self):
    action = self.request.get('action')
    arg_counter = 0;
    args = []
    while True:
      arg = self.request.get('arg' + str(arg_counter))
      arg_counter += 1
      if arg:
        args += (simplejson.loads(arg),);
      else:
        break;
    result = getattr(self, action)(*args)
    self.response.out.write(simplejson.dumps(result))

  def post(self):
    action = self.request.get('action')
    formRequest = self.request
    result = getattr(self, action)(formRequest)
    self.response.out.write(simplejson.dumps(result))

# The RPCs exported to JavaScript follow here:
  
  @authorized.role('admin')
  def FlushAllMemcache(self,flush):
    if flush:
        status = memcache.flush_all()
    cache_stats = memcache.get_stats()
    return cache_stats


  @authorized.role('admin')
  def DeleteSessionToken(self,user_email,target_service):
      stored_token = AuthSubStoredToken.gql('WHERE user_email = :1 and target_service = :2',
          user_email, target_service).get()
      if stored_token:
          stored_token.delete()
      return True

  @authorized.role('admin')
  def UpdateCPediaLog(self,request):
      cpedialog = CPediaLog()
      cpedialog.title = request.get('title')
      cpedialog.author = request.get('author')
      cpedialog.email = request.get('email')
      cpedialog.description = request.get('description')
      cpedialog.root_url = request.get('root_url')
      cpedialog.cache_time = int(request.get('cache_time'))
      cpedialog.logo_images_commas = request.get('logo_images')
      cpedialog.num_per_page = int(request.get('num_per_page'))
      cpedialog.hostIp = request.remote_addr
      cpedialog.local = True
      cpedialog.put()
      return True
