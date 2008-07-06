
import pickle

from google.appengine.ext import db
from google.appengine.ext import search
import logging
import datetime


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
    lastModifiedDate = db.DateTimeProperty()
    lastModifiedBy = db.UserProperty()
    lastCommentedDate = db.DateTimeProperty()
    commentcount = db.IntegerProperty(default=0)
    tags = db.ListProperty(db.Category)
    monthyear = db.StringProperty(multiline=False)
    _weblogId = db.IntegerProperty()   ##for data migration from the mysql system
    assoc_dict = db.BlobProperty()     # Pickled dict for sidelinks, associated Amazon items, etc.
  
    def get_permaink(self):
        if not permalink:
            return permalink
        else:
            return self.date.strftime('%Y/%m/')+str(self.key().id())
  
    def get_tags(self):
        '''comma delimted list of tags'''
        return ','.join([tag for tag in self.tags])
  
    def set_tags(self, tags):
        if tags:
            tagstemp = [db.Category(tag.strip()) for tag in tags.split(',')]
            self.tagsnew = [tag for tag in tagstemp if not tag in self.tags]
            self.tags = tagstemp
  
    tags_commas = property(get_tags,set_tags)

    #for data migration
    def update_archive(self):
        """Checks to see if there is a month-year entry for the
        month of current blog, if not creates it and increments count"""
        my = self.date.strftime('%B %Y') # July 2008
        archive = Archive.all().filter('monthyear',my).fetch(100)
        if archive == []:
            archive = Archive(monthyear=my,date=self.date)
            self.monthyear = my
            self.put()
            archive.put()
        else:
            # ratchet up the count
            archive[0].weblogcount += 1
            archive[0].put()

    def save(self):
        my = self.date.strftime('%B %Y') # July 2008
        self.monthyear = my
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
            self.weblog.lastCommentedDate = datetime.datetime.now()
            self.weblog.commentcount += 1
            self.weblog.put()


