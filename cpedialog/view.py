
import os
import re

import logging

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import copy
import time
import urlparse
import string
import config


class ViewPage(object):
    def __init__(self, cache_time=None):
        """Each ViewPage has a variable cache timeout"""
        if cache_time == None:
            self.cache_time = config.blog['cache_time']
        else:
            self.cache_time = cache_time

    def full_render(self, handler,template_file, params={}):
            url = handler.request.uri
            scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
            template_params = {
                "title": config.blog['title'],
                "current_url": url,
                "user": users.get_current_user(),
                "user_is_admin": users.is_current_user_admin(),
                "login_url": users.create_login_url(handler.request.uri),
                "logout_url": users.create_logout_url(handler.request.uri),
                "BLOG": config.blog, 
            }
            template_params.update(params)
            return template.render(template_file, template_params, debug=config._DEBUG)



    def render_or_get_cache(self, handler, template_file, template_params={}):
        """Checks if there's a non-stale cached version of this view, and if so, return it."""
        if self.cache_time:
            key = handler.request.url + str(users.get_current_user() != None) + str(users.is_current_user_admin())
            output = memcache.get(key)
            if not output:
                logging.debug("Couldn't find a cache for %s", key)
            else:
                logging.debug("Using cache for %s", template_file)
                return output

            output = self.full_render(handler, template_file, template_params)
            # Add a value if it doesn't exist in the cache, with a cache expiration of 1 hour.
            memcache.add(key=key, value=output, time=self.cache_time)
            return output

        return self.full_render(handler, template_file, template_params)


    def render(self, handler,template_name, params={}):
        dirname = os.path.dirname(__file__)
        template_file = os.path.join(dirname, os.path.join('templates', template_name))
        logging.debug("Using template at %s", template_file)
        output = self.render_or_get_cache(handler, template_file, params)
        handler.response.out.write(output)
