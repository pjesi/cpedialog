
import wsgiref.handlers

from google.appengine.ext import webapp

import blog
import album
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
                                        
                                        ('/deleteAllBlog', blog.DeleteAllBlog),
                                        ('/deleteAllBlogReaction', blog.DeleteAllBlogReaction),
                                        ('/loadBlogReactionBulk', blog.LoadBlogReactionBulk),
                                        ('/loadBlogBulk', blog.LoadBlogBulk),
                                        ('/updateArchive', blog.UpdateArchive),

                                        ('/*$', blog.MainPage),
                                        ('/403.html', blog.UnauthorizedHandler),
                                        ('/404.html', blog.NotFoundHandler),
                                        ('/archive/(.*)/*$', blog.ArchiveHandler),
                                        ('/([12]\d\d\d)/(\d|[01]\d)/([-\w]+)/*$', blog.ArticleHandler),
                                        ('/search', blog.SearchHandler),
                                        ('/tag/(.*)', blog.TagHandler),

                                        ('/albums/*$', album.MainPage),
                                        ('/albums/([-\w]+)/([-\w]+)/*$', album.AlbumHandler),
                                        ('/albums/([-\w]+)/([-\w]+)/([\d]+)/*$', album.PhotoHandler),
                                       ],
                                       debug=config._DEBUG)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
