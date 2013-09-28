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
from MyLib import PdfUtils

DU = DirUtils.DirUtils
WS = WebServer.wserver
B  = Book.Book
H = HtmlUtils.HtmlUtils
PB = PdfUtils.PdfBox

urls = (
           "/books", "books",
           "/books/bookshelf/(.*)", "bookshelf",
           "/books/book/(.*)", "book",
           "/books/page/(.*)", "page"
        )

rootpdfdir  = "/home/brad/Documents/Books"
currentwdir = "/home/brad/Documents/Books"
currentbook = None
currentpage = 10
openedbooks = {}

class books:
    dirpath = "/home/brad/Documents/Books/Linux"
    
    def GET(self, dirpath=None):
        global rootpdfdir
        global currentwdir
        # make sure we have something to start with
        winput = web.input(cwd=rootpdfdir)
        cwd = winput.cwd
        if os.path.isdir(cwd):
            currentwdir = cwd
        elif os.path.isfile(cwd):
            currentwdir = os.path.dirname(cwd)
        else:
            currentwdir = rootpdfdir
        du = DU()
        lidirs = du.listAllDirs(currentwdir)
        libooks = du.listAllByExt(".pdf", currentwdir)
        links = []
        for d in lidirs:
            links.append(("/books/bookshelf/?cwd=" + d, d))
        for b in libooks:
            links.append(("/books/book/?bid=" + b, os.path.basename(b[:-4])))
        
        render = web.template.render("templates")
        html = render.main("Your Library", "Your Library", links)
        return html

class bookshelf:

    def GET(self, dirpath):
        global rootpdfdir
        global currentwdir
        # make sure we have something to start with
        winput = web.input(cwd=rootpdfdir)
        cwd = winput.cwd
        if os.path.isdir(cwd):
            currentwdir = cwd
        elif os.path.isfile(cwd):
            currentwdir = os.path.dirname(cwd)
        else:
            currentwdir = rootpdfdir
        # Now we know that we have a valid directory so we can grab all the books and subdirectories
        du = DU()
        lidirs = du.listAllDirs(currentwdir)
        libooks = du.listAllByExt(".pdf", currentwdir)
        links = []
        for d in lidirs:
            links.append(("/books/bookshelf/?cwd=" + d, d))
        for b in libooks:
            links.append(("/books/book/?bid=" + b, os.path.basename(b[:-4])))
        
        render = web.template.render("templates")
        html = render.bookshelf("Your Library", "Your Library", links)
        return html

    
class book:

    def GET(self, bk):
        global currentbook
        global currentpage
        global openedbooks
        winput = web.input()
        currentpage = 10
        abook = None
        if not openedbooks.has_key(winput.bid):
            abook = PB(winput.bid)
            openedbooks[winput.bid] = abook
        else:
            abook = openedbooks[winput.bid]
        currentbook = abook
        text = currentbook.getPage(currentpage)
        footer = [("../page/?pge=%(prv)d" % dict(prv=int(currentpage) - 1), "Previous"), ("../page/?pge=%(nxt)d" % dict(nxt=int(currentpage) + 1), "Next")]
        render = web.template.render("templates")
        html = render.page("Your Library", currentbook.title, text, footer)
        return html
    
class page:
    
    def GET(self, bk):
        global currentbook
        global currentpage
        winput = web.input()
        currentpage = int(winput.pge)
        text = currentbook.getPage(currentpage)
        footer = [("../page/?pge=%(prv)d" % dict(prv=int(currentpage) - 1), "Previous"), ("../page/?pge=%(nxt)d" % dict(nxt=int(currentpage) + 1), "Next")]
        render = web.template.render("templates")
        html = render.page("Your Library", currentbook.title, text, footer)
        return html



if __name__ == "__main__":
    app = WS(urls, globals())
    app.run(9999)