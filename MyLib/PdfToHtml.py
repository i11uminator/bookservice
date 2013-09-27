'''
Created on Sep 15, 2013

@author: root
'''
import os
import subprocess
from MyLib import MyHtmlParser

class PdfHtml(object):
    '''
    classdocs
    '''
    libdir = ""
    filepath = None
    book = None

    def __init__(self, filepath):
        '''
        Constructor
        '''
        self.filepath = filepath
        self.libdir = os.path.dirname(filepath)
        self.book = os.path.basename(filepath)

    def GetHtmlPageBody(self, page):
        html = self.GetHtmlPage(page)
        startidx = html.find("<body")
        if startidx < 0:
            startidx = html.find("<BODY")
        startidx += len("<body")
        startidx += html[startidx:].find(">") + 1
        endidx = html.find("</body>")
        if endidx < 0:
            endidx = html.find("</BODY>")
        if endidx > startidx:
            return html[startidx:endidx]
        return html

        
    def GetHtmlPage(self, page):
        command = "pdftohtml -f %(page)s -l %(page)s -q -noframes -stdout %(book)s" % dict(page=page, book=self.filepath)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        html = p.stdout.readlines()
        outp = "".join(html)
        return self.CleanUpPage(outp)
        
    def CleanUpPage(self, page):
        BT = MyHtmlParser.BadTag
        MHP = MyHtmlParser.MyHTMLParser
        bt1 = BT("hr", [])
        bt2 = BT("meta", ["Content-Type", "UTF-8"])
        bt3 = BT("script", [])
        parser = MHP(page, [bt1, bt2, bt3])
        parser.startParsing()
        return parser.getCleanHtml()