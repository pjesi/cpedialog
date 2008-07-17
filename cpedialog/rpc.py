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

from model import Archive,Weblog,WeblogReactions,AuthSubStoredToken,Album,Menu

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
    request_ = self.request
    result = getattr(self, action)(request_)
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
  def UpdateMenu(self,request):
      menu = Menu.get_by_id(int(request.get("id")))
      editColumn = request.get("editColumn")
      if menu and editColumn:
          newData = request.get("newData")
          if editColumn == "title":
            menu.title = newData
          if editColumn == "permalink":
            menu.permalink = newData
          if editColumn == "target":
            menu.target = newData
          if editColumn == "order":
            menu.order = simplejson.loads(newData)
          if editColumn == "valid":
            menu.valid = simplejson.loads(newData)
          menu.put()        
      return True
        
  @authorized.role('admin')
  def AddMenu(self,request):
      menu = datastore.Entity("Menu")
      menu["title"] = request.get('title')
      menu["permalink"] = request.get('permalink')
      menu["target"] = request.get('target')
      menu["order"] = simplejson.loads(request.get('order'))
      menu["valid"] = simplejson.loads(request.get('valid'))
      datastore.Put(menu)
      menu['key'] = str(menu.key().id())
      return menu

  @authorized.role('admin')
  def DeleteMenu(self,request):
      menu = Menu.get_by_id(int(request.get("id")))
      menu.delete()
      return True

