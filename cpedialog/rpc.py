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
from google.appengine.api import images
from google.appengine.ext import db

from model import Archive,Weblog,WeblogReactions,AuthSubStoredToken,Album,Menu,Images

import authorized
import util

class Image (webapp.RequestHandler):
  def get(self):
    image = db.get(self.request.get("img_id"))
    if image.image:
      self.response.headers['Content-Type'] = "image/png"
      self.response.out.write(image.image)
    else:
      self.response.out.write("No image")

class UploadImage (webapp.RequestHandler):
    @authorized.role('admin')
    def post(self):
        self.response.headers['Content-Type'] = "text/html"
        images = Images()
        img = self.request.get("img")
        if not img:
            self.response.out.write( '{status:"Please select your image."}')
            return
        try:
            images.image = db.Blob(img)
            images.uploader = users.GetCurrentUser()
            key = images.put()
        except Exception, e:
            self.response.out.write( '{status:"An Error Occurred uploading the image."}')
            return
        self.response.out.write('{status:"UPLOADED",image_url:"/rpc/img?img_id=%s"}' % (key))


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

  # for menu inline cell editable table
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
          util.flushMenuList()
      return True
        
  @authorized.role('admin')
  def AddMenu(self,request):
      menu = datastore.Entity("Menu")
      menu["title"] = "New Menu"
      menu["permalink"] = "New permalink"
      menu["target"] = "_self"
      menu["order"] = 0
      menu["valid"] = False
      datastore.Put(menu)
      util.flushMenuList()
      menu['key'] = str(menu.key())
      menu['id'] = str(menu.key().id())
      return menu

  @authorized.role('admin')
  def DeleteMenu(self,request):
      menu = Menu.get_by_id(int(request.get("id")))
      menu.delete()
      util.flushMenuList()
      return True

  # for album inline cell editable table.
  @authorized.role('user')
  def UpdateAlbum(self,request):
      album = Album.get_by_id(int(request.get("id")))
      editColumn = request.get("editColumn")
      if album and editColumn:
          newData = request.get("newData")
          if editColumn == "album_username":
            album.album_username = newData
          if editColumn == "album_type":
            album.album_type = newData
          if editColumn == "access":
            album.access = newData
          if editColumn == "date":
            album.date = simplejson.loads(newData)
          if editColumn == "valid":
            album.valid = simplejson.loads(newData)
          album.put()
          util.flushAlbumList()
      return True

  @authorized.role('user')
  def AddAlbum(self,request):
      album = datastore.Entity("Album")
      album["album_username"] = "New Album"
      album["album_type"] = "public"
      album["access"] = "public"
      album["date"] = datetime.datetime.now()
      album["valid"] = False
      album["owner"] = users.GetCurrentUser()
      datastore.Put(album)
      util.flushAlbumList()
      album['key'] = str(album.key())
      album['id'] = str(album.key().id())
      album["date"] = album["date"].strftime('%m/%d/%y')
      album["owner"] = str(album["owner"].email())
      return album

  @authorized.role('user')
  def DeleteAlbum(self,request):
      album = Album.get_by_id(int(request.get("id")))
      album.delete()
      util.flushAlbumList()
      return True

