'''
Created on Sep 15, 2013

@author: brad
'''

from HTMLParser import HTMLParser
import types
from MyLib import StringUtils
from MyLib import HtmlUtils

class BadTag(object):
    tag = ""
    excuses = []
    def __init__(self, tag, excuse):
        self.tag = tag
        self.excuses = excuse
        
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    cleanhtml = ""
    dirtyhtml = ""
    keep = True
    badtag = False
    currentBadTag = None
    badtags = []
    
    def __init__(self, html, btags = []): 
        HTMLParser.__init__(self)
        cleanme = html
        for b in btags:
            self.badtags.append(b)
            hu = HtmlUtils.HtmlUtils()
            partiallycleaned = hu.close_all_open_first(cleanme, "<"+b.tag+">")
            cleanme = hu.close_open_tags(partiallycleaned, "<"+b.tag+">")
        self.dirtyhtml = cleanme
        
    def startParsing(self):
        self.feed(self.dirtyhtml)

    def setBadTags(self, tags): 
        for t in tags:
            t.tag = t.tag.lower()
            self.badtags.append(t)
            hu = HtmlUtils.HtmlUtils()
            self.dirtyhtml = hu.close_all_open_first(self.dirtyhtml, "<" + t.tag + ">")
            self.dirtyhtml = hu.close_open_tags(self.dirtyhtml, "<" + t.tag + ">")

    def hasAnException(self, excuse, attrs):            
        for e in excuse.excuses:
            for a in attrs:
                if e in a or e == a:
                    return True
        return False
    
    def handle_starttag(self, tag, attrs):
        if not self.badtag and self.isKeepable(tag, attrs): # Make sure we're not still parsing bad shit...
            cleaned = ""
            att = ""
            if attrs:
                for x in attrs:
                    if len(x) >= 2:
                        att = "%s %s='%s'" % (att, x[0], x[1])
            cleaned = "<%s%s>" % (tag, att)
            self.cleanhtml = "%s %s" % (self.cleanhtml, cleaned)

    def handle_endtag(self, tag):
        if self.badtag == True:
            # We're looking for the endtag that matches self.currentBadTag so we can start keeping again
            if tag == self.currentBadTag:
                self.currentBadTag = None
                self.badtag = False
                self.keep = True
        else:
            self.cleanhtml += "</%s>" % tag
    
    def handle_data(self, data):
        if self.keep:
            self.cleanhtml = "%s %s" % (self.cleanhtml, data)

        
    def isBadTag(self, tag):
        for t in self.badtags:
            if t.tag.lower() == tag.lower():
                return True 
        return False

    def getTagByName(self, tag):
        for t in self.badtags:
            if tag.lower() == t.tag.lower():
                return t
    
    def isKeepable(self, tag, attrs):
        # determine whether we want the html
        if self.badtag:
            # we're already parsing within a bad tag so...
            return False
        else:
            if self.isBadTag(tag) and not self.hasAnException(self.getTagByName(tag), attrs):
                self.currentBadTag = tag
                self.keep = False
                self.badtag = True
                return False
            else:
                return True
            
    def getCleanHtml(self):
        return self.cleanhtml