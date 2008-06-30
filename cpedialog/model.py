
import pickle

from google.appengine.ext import db
from google.appengine.ext import search
import logging


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
  _weblogId = db.IntegerProperty()   ##for data migration from the mysql system
  tags = db.ListProperty(db.Category)
  assoc_dict = db.BlobProperty()     # Pickled dict for sidelinks, associated Amazon items, etc.

  def get_permaink(self):
      if not permalink:
          return permalink
      else:
          return self.date.strftime('%Y/%m/')+str(self.key().id())

  # Serialize data that we'd like to store with this article.
  # Examples include relevant (per article) links and associated Amazon items.
  def set_associated_data(self, data):
      self.assoc_dict = pickle.dumps(data)

  def get_associated_data(self):
      return pickle.loads(self.assoc_dict)

  def rfc3339_published(self):
      return self.date.strftime('%Y-%m-%dT%H:%M:%SZ')

  def rfc3339_updated(self):
      return self.lastModifiedDate.strftime('%Y-%m-%dT%H:%M:%SZ')

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
  userIp = db.StringProperty()
  content = db.TextProperty()
  lastModifiedDate = db.DateTimeProperty()
  lastModifiedBy = db.UserProperty()
  _weblogReactionId = db.IntegerProperty()   ##for data migration from the mysql system


