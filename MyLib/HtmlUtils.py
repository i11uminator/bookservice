'''
Created on Sep 22, 2013

@author: root
'''
from MyLib import StringUtils

class HtmlUtils(object):
    
    def insertHtml(self, html, text, tag):
        li = html.split(tag.lower())
        if len(li) < 2:
            li = html.split(tag.upper())
        rethtml = (text + tag).join(li)
        return rethtml
    
    def insertBeforeTag(self, html, text, tag):
        return self.insertHtml(html, text, tag)
    
    def insertAfterTag(self, html, text, tag):
        li = html.split(tag.lower())
        if len(li) < 2:
            li = html.split(tag.upper())
        rethtml = (tag + text).join(li)
        return rethtml
    
    def insertAfterNthTag(self, html, text, tag, occurance):
        replacewith = (tag + text)
        su = StringUtils.StringUtils()
        su.replaceNthOccurance(html, tag, replacewith, occurance)
    
    def insertBeforeNthTag(self, html, text, tag, occurance):
        replacewith = (text + tag)
        su = StringUtils.StringUtils()
        su.replaceNthOccurance(html, tag, replacewith, occurance)

    def addFooter(self, html, footer):
        return self.insertHtml(html, footer, "</body>")
        
    def close_all_open_first(self, text, tag):
        closedtag = "</" + tag[1:]
        su = StringUtils.StringUtils()
        opens = su.findAllOccurances(text, tag)
        closeds = su.findAllOccurances(text, closedtag)
        if len(closeds) == 0:
            if len(opens) > 2 and len(opens) % 2 != 0:
                opens = opens[:-1]
            cleaned = text
            for l in xrange(len(opens)):
                if l % 2 != 0:
                    cleaned = su.replaceNthOccurance(cleaned, tag, closedtag, l + 1)
        return cleaned
            
    def close_open_tags(self, text, tag):
        closedtag = "</" + tag[1:]
        su = StringUtils.StringUtils()
        opens = su.findAllOccurances(text, tag)
        closeds = su.findAllOccurances(text, closedtag)
        cleaned = text
        while len(opens) > len(closeds):
            cleaned = su.replaceNthOccurance(cleaned, tag, "", len(opens))
            opens = opens[:-1]
        while len(closeds) > len(opens):
            cleaned = su.replaceNthOccurance(cleaned, closedtag, "", len(closeds))
            closeds = closeds[:-1]
        n = 1
        for o, c in zip(opens, closeds):
            if o > c:
                cleaned = su.replaceNthOccurance(cleaned, tag, closedtag, n)
                cleaned = su.replaceNthOccurance(cleaned, closedtag, tag, n)    
                n = n + 1
        if n > 1:
            cleaned = self.close_open_tags(cleaned, tag)
        return cleaned