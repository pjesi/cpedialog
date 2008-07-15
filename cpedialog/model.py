__author__ = 'Ping Chen'


import pickle

from google.appengine.ext import db
from google.appengine.ext import search
import logging
import datetime
import urllib
import config


class Archive(db.Model):
    monthyear = db.StringProperty(multiline=False)
    """July 2008"""
    weblogcount = db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)

class Tag(db.Model):
    tag = db.StringProperty(multiline=False)
    tagcount = db.IntegerProperty(default=0)


class Weblog(db.Model):
    permalink = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty()
    authorEmail = db.EmailProperty()
    catalog = db.StringProperty()
    lastCommentedDate = db.DateTimeProperty()
    commentcount = db.IntegerProperty(default=0)
    lastModifiedDate = db.DateTimeProperty()
    lastModifiedBy = db.UserProperty()
    tags = db.ListProperty(db.Category)
    monthyear = db.StringProperty(multiline=False)
    entrytype = db.StringProperty(multiline=False,default='post',choices=[
        'post','page'])
    _weblogId = db.IntegerProperty()   ##for data migration from the mysql system
    assoc_dict = db.BlobProperty()     # Pickled dict for sidelinks, associated Amazon items, etc.
  
    def get_permaink(self):
        if not permalink:
            return permalink
        else:
            return self.date.strftime('%Y/%m/')+str(self.key().id())

    def full_permalink(self):
        return config.blog['root_url'] + '/' + self.permalink

    def get_tags(self):
        '''comma delimted list of tags'''
        return ','.join([urllib.unquote(tag) for tag in self.tags])
  
    def set_tags(self, tags):
        if tags:
            tagstemp = [db.Category(urllib.quote(tag.strip().encode('utf8'))) for tag in tags.split(',')]
            self.tagsnew = [tag for tag in tagstemp if not tag in self.tags]
            self.tags = tagstemp
  
    tags_commas = property(get_tags,set_tags)

    #for data migration
    def update_archive(self):
        """Checks to see if there is a month-year entry for the
        month of current blog, if not creates it and increments count"""
        my = self.date.strftime('%B %Y') # July 2008
        archive = Archive.all().filter('monthyear',my).fetch(10)
        if archive == []:
            archive = Archive(monthyear=my,date=self.date,weblogcount=1)
            archive.put()
        else:
            # ratchet up the count
            archive[0].weblogcount += 1
            archive[0].put()

    def save(self):
        if self.entrytype == "post":
            self.update_archive()
        my = self.date.strftime('%B %Y') # July 2008
        self.monthyear = my
        self.put()


class WeblogReactions(db.Model):
    weblog = db.ReferenceProperty(Weblog)
    user = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty()
    authorEmail = db.EmailProperty()
    authorWebsite = db.StringProperty()
    userIp = db.StringProperty()
    content = db.TextProperty()
    lastModifiedDate = db.DateTimeProperty()
    lastModifiedBy = db.UserProperty()
    _weblogReactionId = db.IntegerProperty()   ##for data migration from the mysql system

    def save(self):
        self.put()
        if self.weblog is not None:
            self.weblog.lastCommentedDate = self.date
            self.weblog.commentcount += 1
            self.weblog.put()


class AuthSubStoredToken(db.Model):
  user_email = db.StringProperty(required=True)
  target_service = db.StringProperty(multiline=False,default='base',choices=[
        'apps','base','blogger','calendar','codesearch','contacts','docs',
        'albums','spreadsheet','youtube'])
  session_token = db.StringProperty(required=True)


#System configuration.
class CPediaLog(db.Model):
   title = db.StringProperty()
   author = db.StringProperty()
   email = db.StringProperty()
   description = db.StringProperty()
   root_url = db.StringProperty()
   cache_time = db.IntegerProperty(default=0)
   logo_images = db.ListProperty(db.Category)
   debug_mode = db.BooleanProperty()
   num_per_page = db.IntegerProperty(default=8)
   hostIp = db.StringProperty()    
   local = db.BooleanProperty()

   def get_logo_images(self):
       '''comma delimted list of tags'''
       return ','.join([urllib.unquote(logo_image) for logo_image in self.logo_images])

   def set_logo_images(self, logo_images):
       if tags:
           logo_imagestemp = [db.Category(urllib.quote(logo_image.strip().encode('utf8'))) for logo_image in logo_images.split(',')]
           self.logo_imagesnew = [logo_image for logo_image in logo_imagestemp if not logo_image in self.logo_images]
           self.logo_images = logo_imagestemp
  
   logo_images_commas = property(get_logo_images,set_logo_images)

class Album(db.Model):
    username = db.StringProperty()
    owner = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    private = db.BooleanProperty()
