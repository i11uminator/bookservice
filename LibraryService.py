'''
Created on Sep 22, 2013

@author: root
'''

import web
import os
from MyLib import DirUtils
from MyLib import WebServer
from MyLib import Book
from MyLib import HtmlUtils

DU = DirUtils.DirUtils
WS = WebServer.wserver
B  = Book.Book
H = HtmlUtils.HtmlUtils

urls = (
           "/books", "books",
           "/books/bookshelf", "bookshelf",
           "/books/book/(.*)", "book",
           "/books/page/(.*)", "page"
        )

currentwdir = "/home/brad/Documents/Books"
currentbook = None
currentpage = 10

class books:
    dirpath = "/home/brad/Documents/Books/Linux"
    
    def GET(self):
        du = DU()
        libooks = du.listAllByExt(".pdf", self.dirpath)
        html = "<html><head><title>Your library</title><script></script></head><body>"
        for b in libooks:
            html += "<a href='books/book/?bid=%(pdf)s'>%(title)s</a><br/>" % dict(pdf=b, title=os.path.basename(b)[:-4])
        html += "</body></html>"
        return html

class bookshelf:
    def Get(self, dirpath):
        global currentwdir
    
class book:

    def GET(self, bk):
        global currentbook
        global currentpage
        winput = web.input()
        currentpage = 10
        currentbook = B(winput.bid, currentpage)
        html = currentbook.getPage()
        footer = "<p><a href='../page/?pge=9'>Previous</a></p><p><a href='../page/?pge=11'>Next</a></p>"
        h = H()
        html = h.addFooter(html, footer)
        return html
    
class page:
    
    def GET(self, bk):
        global currentbook
        global currentpage
        winput = web.input()
        currentpage = winput.pge
        html = currentbook.getPage(currentpage)
        footer = "<p><a href='../page/?pge=%(prv)d'>Previous</a></p><p><a href='../page/?pge=%(nxt)d'>Next</a></p>" % dict(prv=int(currentpage) - 1, nxt=int(currentpage) + 1)
        h = H()
        html = h.addFooter(html, footer)
        return html



if __name__ == "__main__":
    app = WS(urls, globals())
    app.run(9999)