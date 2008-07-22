__author__ = 'Ping Chen'

import wsgiref.handlers

from google.appengine.ext import webapp

import rpc
import blog
import album
import admin
import logging
import config

from google.appengine.ext.webapp import template
template.register_template_library('cpedia.filter.replace')


def main():

    application = webapp.WSGIApplication(
                                       [('/addBlog', blog.AddBlog),
                                        ('/viewBlog', blog.ViewBlog),
                                        ('/addBlogReaction', blog.AddBlogReaction),
                                        ('/editBlog', blog.EditBlog),
                                        ('/deleteBlog', blog.DeleteBlog),
                                        ('/editBlogReaction', blog.EditBlogReaction),
                                        ('/deleteBlogReaction', blog.DeleteBlogReaction),

                                        ('/admin/*$', admin.MainPage),
                                        ('/rpc', rpc.RPCHandler),
                                        ('/rpc/uploadImage', rpc.UploadImage),
                                        ('/rpc/img', rpc.Image),

                                        ('/*$', blog.MainPage),
                                        ('/403.html', blog.UnauthorizedHandler),
                                        ('/404.html', blog.NotFoundHandler),
                                        ('/archive/(.*)/*$', blog.ArchiveHandler),
                                        ('/([12]\d\d\d)/(\d|[01]\d)/([-\w]+)/*$', blog.ArticleHandler),
                                        ('/search', blog.SearchHandler),
                                        ('/tag/(.*)', blog.TagHandler),
                                        ('/delicious/(.*)', blog.DeliciousHandler),
                                        ('/atom/*$', blog.FeedHandler),
                                        ('/sitemap/*$', blog.SiteMapHandler),  #for live.com SEO

                                        ('/albums/*$', album.MainPage),
                                        ('/albums/([-\w\.]+)/*$', album.UserHandler),
                                        ('/albums/([-\w\.]+)/([-\w]+)/*$', album.AlbumHandler),
                                        ('/albums/([-\w\.]+)/([-\w]+)/([\d]+)/*$', album.PhotoHandler),

                                        ('/([-\w]+)/*$', blog.PageHandler),                                        
                                       ],
                                       debug=config._DEBUG)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
