'''
Created on Sep 21, 2013

@author: Brad Kline
'''

import os
from MyLib import PdfToHtml
from MyLib import StringUtils
from MyLib import HtmlUtils

class Book(object):
    currentpage = None
    filepath = "" 
    title = ""
    dirpath = ""
    
    def __init__(self, filepath, page = None):
        self.filepath = filepath
        self.title = os.path.basename(filepath)
        self.dirpath = os.path.dirname(filepath)
        self.currentpage = page
        
    def getPage(self, page = None):
        if page == None:
            page = (self.currentpage, 10)[self.currentpage == None]
        PH = PdfToHtml.PdfHtml
        mph = PH(self.filepath)
        page = mph.GetHtmlPage(page)
        page = self.fixLinks(page)
        return page
    
    def getPageBody(self, page = None):
        if page == None:
            page = (self.currentpage, 10)[self.currentpage == None]
        PH = PdfToHtml.PdfHtml
        mph = PH(self.filepath)
        page = mph.GetHtmlPageBody(page)
        page = self.fixLinks(page)
        return page
    
    def fixLinks(self, page):
        su = StringUtils.StringUtils()
        lnk = self.title[:-(len(".pdf"))] + ".html#"
        li = su.findAllOccurances(page, lnk)
        if len(li) > 0:
            page = su.rreplace(page, lnk, "../page/?pge=", len(li))
        return page
    
    def getContents(self):
        print("Not implemented!")
        
    def getNumberOfPages(self):
        print("Not implemented!")