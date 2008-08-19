__author__ = 'Ping Chen'

blog = {
    "title": "CPEDIA's Blog",
    "author": "Ping Chen",
    "email": "cpedia@gmail.com",   # This must be the email address of a registered administrator for the application due to mail api restrictions.
    "description": "CPEDIA's Blog powered by Google AppEngine.",
    "root_url": "http://blog.cpedia.com",
    "cache_time": 0,      # You can override this default for each page through a handler's call to view.ViewPage(cache_time=...)

    #apply google ajax feed key for your domain from: http://code.google.com/apis/ajaxfeeds/signup.html
    "google_ajax_feed_enable":True,
    "google_ajax_feed_key":"ABQIAAAAOY_c0tDeN-DKUM-NTZldZhQG0TqTy2vJ9mpRzeM1HVuOe9SdDRSieJccw-q7dBZF5aGxGJ-oZDyf5Q",
    "google_ajax_feed_result_num":15,
    "google_ajax_feed_title":"Technical Articles",

    "delicious_enable":True,
    "delicious_username":"cpedia",

    "recaptcha_enable":True,
    "recaptcha_public_key":"6Ld7tQIAAAAAAJLo39p3u6AvTAJcXftc5mJeAif5",
    "recaptcha_private_key":"6Ld7tQIAAAAAAO0iDvyai5Ie-WUHuyDwpshIlKro",

    "logo_images": ["http://blog.cpedia.com/img/logo/logo1.gif",
                    "http://blog.cpedia.com/img/logo/logo2.gif"],

    "debug":True,
    "num_post_per_page":8
}

delicious = {
    "username":"cpedia"    #del.icio.us user name.
}

recaptcha = {
    "enable":True,
    "public_key":"6Ld7tQIAAAAAAJLo39p3u6AvTAJcXftc5mJeAif5",  #you get get recaptcha key for your domain from:http://recaptcha.net/
    "private_key":"6Ld7tQIAAAAAAO0iDvyai5Ie-WUHuyDwpshIlKro"  
}

logo_images = ["http://blog.cpedia.com/img/logo/logo1.gif",
               "http://blog.cpedia.com/img/logo/logo2.gif"]

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

#entity num of per page.
_NUM_PER_PAGE = 8
