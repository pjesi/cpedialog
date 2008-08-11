__author__ = 'Ping Chen'

blog = {
    "title": "CPEDIA's Blog",
    "author": "Ping Chen",
    "email": "cpedia@gmail.com",   # This must be the email address of a registered administrator for the application due to mail api restrictions.
    "description": "CPEDIA's Blog powered by Google AppEngine.",
    "root_url": "http://blog.cpedia.com",
    "cache_time": 0,      # You can override this default for each page through a handler's call to view.ViewPage(cache_time=...)
}

album ={
    "username":["cpedia","yeli.piao","pegina8"]
}

delicious = {
    "username":"cpedia"    #del.icio.us user name.
}

google_docs = {
    "username":"cpedia@gmail.com"
}

google_calendar = {
    "username":"cpedia@gmail.com"
}

recaptcha = {
    "enable":True,
    "public_key":"6Ld7tQIAAAAAAJLo39p3u6AvTAJcXftc5mJeAif5",  #you get get recaptcha key for your domain from:http://recaptcha.net/
    "private_key":"6Ld7tQIAAAAAAO0iDvyai5Ie-WUHuyDwpshIlKro"  
}

logo_images = ["logo1.gif","logo2.gif"]  #make sure the images located in the folder img/logo.

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

#entity num of per page.
_NUM_PER_PAGE = 8
