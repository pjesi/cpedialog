
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
        self.update_archive()
        my = self.date.strftime('%B %Y') # July 2008
        self.monthyear = my
        self.lastCommentedDate = datetime.datetime(1980, 1, 1, 23, 59, 59) #for data migration.
        self.entrytype = 'post'
        self.put()
  
  
    # Serialize data that we'd like to store with this article.
    # Examples include relevant (per article) links and associated Amazon items.
    def set_associated_data(self, data):
        self.assoc_dict = pickle.dumps(data)
  
    def get_associated_data(self):
        return pickle.loads(self.assoc_dict)
  
    def is_big(self):
        if len(self.content) > 2000 or '<img' in self.content or '<code>' in self.content or '<pre>' in self.content:
            return True
        else:
            return False


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
