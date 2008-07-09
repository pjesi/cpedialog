__author__ = 'Ping Chen'


from google.appengine.api import users
from google.appengine.ext import db

import urllib

from model import AuthSubStoredToken

def role(role):
    """A decorator to enforce user roles, currently 'user' (logged in) and 'admin'.

    To use it, decorate your handler methods like this:

    import authorized
    @authorized.role("admin")
    def get(self):
      user = users.GetCurrentUser(self)
      self.response.out.write('Hello, ' + user.nickname())

    If this decorator is applied to a GET handler, we check if the user is logged in and
    redirect her to the create_login_url() if not.

    For HTTP verbs other than GET, we cannot do redirects to the login url because the
    return redirects are done as GETs (not the original HTTP verb for the handler).  
    So if the user is not logged in, we return an error.
    """
    def wrapper(handler_method):
        def check_login(self, *args, **kwargs):
            user = users.get_current_user()
            if not user:
                if self.request.method != 'GET':
                    self.error(403)
                else:
                    self.redirect(users.create_login_url(self.request.uri))
            elif role == "user" or (role == "admin" and users.is_current_user_admin()):
                handler_method(self, *args, **kwargs)
            else:
                if self.request.method == 'GET':
                    self.redirect("/403.html")
                else:
                    self.error(403)   # User didn't meet role.
        return check_login
    return wrapper


def authSub(service):
    def wrapper(handler_method):
        def check_authSub(self, *args, **kwargs):
            user = users.get_current_user()
            if not user:
                if self.request.method != 'GET':
                    self.error(403)
                else:
                    self.redirect(users.create_login_url(self.request.uri))
            else:
                client = gdata.service.GDataService()
                token =  LookupToken(client, user.email(),service)
                if token is Null:
                    next = self.request.uri
                    query = {"service":service}
                    next += next.count('?') and '&amp;' or '?'+urllib.urlencode(query)                    
                    auth_sub_url = gdata.service.GDataService().GenerateAuthSubURL(next, scope[service],
                        secure=False, session=True)
                    self.redirect(auth_sub_url)
                else:
                    for param in self.request.query.split('&'):
                      # Get the token scope variable we specified when generating the URL
                      if param.startswith('token_scope'):
                        token_scope = urllib.unquote_plus(param.split('=')[1])
                      # Google Data will return a token, get that
                      elif param.startswith('token'):
                        token = param.split('=')[1]
                      # Find out what the target URL is that we should attempt to fetch.
                      elif param.startswith('feed_url'):
                        feed_url = urllib.unquote_plus(param.split('=')[1])

                      # If we received a token for a specific feed_url and not a more general
                      # scope, then use the exact feed_url in this request as the scope for the
                      # token.
                      if token and feed_url and not token_scope:
                        token_scope = feed_url

                    #update the token into db.

                    try:
                        handler_method(self, *args, **kwargs)
                    except gdata.service.RequestError, request_error:
                      # If fetching fails, then tell the user that they need to login to
                      # authorize this app by logging in at the following URL.
                      if request_error[0]['status'] == 401:
                        # Get the URL of the current page so that our AuthSub request will
                        # send the user back to here.
                        next = self.request.uri
                        auth_sub_url = client.GenerateAuthSubURL(next, feed_url,
                            secure=False, session=True)
                        self.redirect(users.create_login_url(auth_sub_url))
                      else:
                        self.error(403)



                # Stores the page's current user
                current_user = None
                # Stores the token_scope information
                token_scope = None
                # Stores the Google Data Client
                client = None
                # The one time use token value from the URL after the AuthSub redirect.
                token = None
                # Feed URL which should be fetched by the gdata client.
                feed_url = None

                for param in self.request.query.split('&'):
                  # Get the token scope variable we specified when generating the URL
                  if param.startswith('token_scope'):
                    token_scope = urllib.unquote_plus(param.split('=')[1])
                  # Google Data will return a token, get that
                  elif param.startswith('token'):
                    token = param.split('=')[1]
                  # Find out what the target URL is that we should attempt to fetch.
                  elif param.startswith('feed_url'):
                    feed_url = urllib.unquote_plus(param.split('=')[1])

                  # If we received a token for a specific feed_url and not a more general
                  # scope, then use the exact feed_url in this request as the scope for the
                  # token.
                  if token and feed_url and not token_scope:
                    token_scope = feed_url

                  # Manage our Authentication for the user
                  ManageAuth()
                  LookupToken()


                next = self.request.uri
                auth_sub_url = gdata.service.GDataService().GenerateAuthSubURL(next, self.feed_url,
                    secure=False, session=True)



        return check_authSub
    return wrapper

def ManageAuth(self):
  self.client = gdata.service.GDataService()
  if self.token:
    # Upgrade to a session token and store the session token.
    self.UpgradeAndStoreToken()

def UpgradeAndStoreToken(self):
  self.client.SetAuthSubToken(self.token)
  self.client.UpgradeToSessionToken()
  if self.current_user:
    # Create a new token object for the data store which associates the
    # session token with the requested URL and the current user.
    new_token = StoredToken(user_email=self.current_user.email(),
        session_token=self.client.GetAuthSubToken(),
        target_url=self.token_scope)
    new_token.put()

def LookupToken(client, email, service):
    #todo:get the cached token.
    stored_tokens = AuthSubStoredToken.gql('WHERE user_email = :1 and target_service = :2',
        email, service)
    for token in stored_tokens:
      if self.feed_url.startswith(token.target_url):
        client.SetAuthSubToken(token.session_token)
        return


scope = {
    "calendar":"http://www.google.com/calendar/feeds/",
    "docs":"http://docs.google.com/feeds/",
    "albums":"http://picasaweb.google.com/data/feed/",
    "blogger":"http://www.blogger.com/feeds/",
    "base":"http://www.google.com/base/feeds/",
    "site":"https://www.google.com/webmasters/tools/feeds/",
    "spreadsheets":"http://spreadsheets.google.com/feeds/",
    "codesearch":"http://www.google.com/codesearch/feeds/",
    "finance":"http://finance.google.com/finance/feeds/",
    "contacts":"http://www.google.com/m8/feeds/",
    "youtube":"http://gdata.youtube.com/feeds/",
}