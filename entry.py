'''
Created on Sep 15, 2013

@author: brad
'''

from MyLib import MyHtmlParser
from MyLib import PdfToHtml

M = MyHtmlParser.MyHTMLParser
B = MyHtmlParser.BadTag
P = PdfToHtml
PH = P.PdfHtml
 
# dirtyhtml = None
# 
# with open("/home/brad/Programming/Python/pserv/test3.html", "r") as myfile:
#     dirtyhtml = myfile.read()
#     
# b1 = B("script", [])
# b2 = B("meta", ["Content-Type", "UTF-8"])
# b3 = B("hr", [])
# 
# mhp = M(dirtyhtml,  [b1, b2, b3])
# #mhp.dirtyhtml = mhp.close_all_open_first(mhp.dirtyhtml, "<hr>", ["script", "hr", "meta"])
# mhp.startParsing()
# cleanhtml = ""
# 
# cleanhtml = mhp.getCleanHtml()
# 
# print(cleanhtml)
# 
# with open("/home/brad/Programming/Python/pserv/testout.html", "w") as myfile:
#     myfile.write(cleanhtml)
# 
# print("done bitches!")
# 
#     

# ph = PH("/home/brad/Documents/Books/Linux/Linux-101-Hacks.pdf")

ph = PH("/home/brad/Documents/Books/Programing/Csharp/C#InDepth.pdf")
html = ph.GetHtmlPage(77)
print(html)

with open("/home/brad/Programming/Python/pserv/testout.html", "w") as myfile:
    myfile.write(html)
    

