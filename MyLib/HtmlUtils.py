'''
Created on Sep 22, 2013

@author: root
'''
from MyLib import StringUtils
import types

class HtmlUtils(object):
    attrs = ""
    emptycells = ""
    
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
        return su.replaceNthOccurance(html, tag, replacewith, occurance)
    
    def insertBeforeNthTag(self, html, text, tag, occurance):
        replacewith = (text + tag)
        su = StringUtils.StringUtils()
        return su.replaceNthOccurance(html, tag, replacewith, occurance)

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
    
    def getHyperLink(self, dest, title):
        return "<a href='%(dest)s'>%(title)s</a>" % dict(dest=dest, title=title)
    
    def getTable(self, data, columns, headers = []):
        if len(data) > 0:
            html = "<table %(attrs)s>" % dict(attrs=self.attrs)
            if headers and len(headers) == columns:
                html += "<tr>"
                for h in headers:
                    html += "<th>%s</th>" % h
                html += "</tr>"
            if columns == 0:
                columns = 2
            idx = 0
            while idx < len(data):
                html += "<tr>"
                for d in range(columns):
                    if idx < len(data):
                        html += "<td>%s</td>" % data[idx]
                    else:
                        html += "<td>%s</td>" % self.emptycells
                    idx += 1
                html += "</tr>"
            html += "</table>"
            return html

    def setAttrs(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.attrs += "%(key)s='%(value)s' " % dict(key=key, value=value)
            
    def insertRows(self, table, rows, slot):
        # Insert rows into table at slot
        su = StringUtils.StringUtils()
        trows = len(su.findAllOccurances(table, "<tr>"))
        # we'll just append the rows if the requested slot is too large
        if slot > trows + 1:
            slot = trows  
        html = ""
        # if we've been given a string to insert
        # however, the caller must ensure that the column-number is correct!
        # TODO - We should probably check...
        if isinstance(rows, basestring):
            html = self.insertAfterNthTag(table, rows, "</tr>", slot)
        elif isinstance(rows, list):
            # find largest number of columns if we've been given a list
            lirows = table.split("<tr>")
            c = 0
            for cr in lirows:
                rc = len(su.findAllOccurances(cr, "<td>"))
                if c < rc:
                    c = rc
            # now create the rows
            newrows = self.getTableRows(rows, c)
            html = self.insertAfterNthTag(table, newrows, "</tr>", slot)
        return html
            
            
    def getTableRow(self, data, isheader = False):
        otag = "<td>"
        ctag = "</td>"
        if isheader:
            otag = "<th>"
            ctag = "</th>"
        html = "<tr>"
        for d in data:
            html += "%(otag)s%(text)s%(ctag)s" % dict(otag=otag, text=d, ctag=ctag)
        html += "</tr>"
        return html
        
    def getTableRows(self, data, columns):
        if len(data) > 0:
            if columns == 0:
                columns = 1
            idx = 0
            html = ""
            while idx + columns < len(data):
                html += self.getTableRow(data[idx:idx+columns])
                idx += columns
            while idx + columns > len(data):
                data.append(self.emptycells)
            html += self.getTableRow(data[idx:idx+columns])
            return html


test = True

if test:
    hu = HtmlUtils()
    hlinks =[ 
              hu.getHyperLink("/books/book", "one"), 
              hu.getHyperLink("/books/book", "two"), 
              hu.getHyperLink("/books/book", "three"),
              hu.getHyperLink("/books/book", "four"),
              hu.getHyperLink("/books/book", "five"),
              hu.getHyperLink("/books/book", "six"),
              hu.getHyperLink("/books/book", "seven")
              
            ]
    html = hu.getTable( hlinks, 3, [ "c1", "c2", "c3" ] )
    hlinks2 = hlinks[:-2]
    attrs = { "border":"2", "cellpadding":"10" }
    hu.setAttrs(**attrs)
    html2 = hu.getTable(hlinks2, 3)
    html3 = "<table>%s</table>" % hu.getTableRows(hlinks[2:-1], 3)
    html4 = hu.insertRows(html2, hlinks2, 2)
    
    print(html)
    print("-----------------------------")
    print("-----------------------------")
    print(html2)
    print("-----------------------------")
    print("-----------------------------")
    print(html3)
    print("-----------------------------")
    print("-----------------------------")
    print(html4)