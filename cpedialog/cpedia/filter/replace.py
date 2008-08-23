import re
from google.appengine.ext import webapp

import urllib
import re
import cgi



register = webapp.template.create_template_register()


@register.filter
def replace ( string, args ):
        search  = args[0]
        replace = args[1]
        return re.sub( search, replace, string )

@register.filter
def email_username ( email ):
        return email.split("@")[0]

@register.filter
def unquote ( str ):
        return urllib.unquote(str.encode('utf8'))

@register.filter
def quote ( str ):
        return urllib.quote(str)

@register.filter
def escape ( str ):
        return cgi.escape(str)

