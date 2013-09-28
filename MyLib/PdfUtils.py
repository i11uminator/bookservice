'''
Created on Sep 27, 2013

@author: root
'''

from pyPdf import PdfFileReader

class PdfBox(object):
    ''' Wraps pyPdf utils into a pdf object'''
    pdfReader = None
    pdfInfo = None
    extractedPages = {}
    filepath = ""
    isencrypted = False
    password = ""
    author = ""
    title = ""
    subject = ""
    pages = 0
    initialized = False

    def __init__(self, filepath, password = None):
        self.filepath = filepath
        self.pdfReader = PdfFileReader(file(filepath, "rb"))
        if password:
            self.password = password
        if self.initializePdf(self.password):
            self.pdfInfo = self.pdfReader.getDocumentInfo()
            self.author = self.pdfInfo.author
            self.title = self.pdfInfo.title
            self.pages = self.pdfReader.getNumPages()
            self.subject = self.pdfInfo.subject
            self.extractedPages = {}
        
    def initializePdf(self, password = None):
        if self.pdfReader.getIsEncrypted():
            self.isencrypted = True
            if self.pdfReader.decrypt(self.password):
                self.initialized = True
                return True
        else:
            self.initialized = True
            return True
        return False
    
    def getPage(self, pagenum):
        if self.extractedPages.has_key(pagenum):
            return self.extractedPages[pagenum]
        else:
            page = self.pdfReader.getPage(pagenum)
            text = page.extractText()
            self.extractedPages[pagenum] = text
            return text

Test = False
if Test:
    pdfpath = "/home/brad/Documents/Books/Linux/Linux-101-Hacks.pdf"
    pdfpath2 = "/home/brad/Documents/Books/Linux/Linux_Pocket_Guide.pdf"
    pdf = PdfBox(pdfpath, "")
    pdf2 = PdfBox(pdfpath2, "")
    info = "%(title)s, - %(subject)s written by %(author)s has %(pages)d" % dict(title=pdf.title, subject=pdf.subject, author=pdf.author, pages=pdf.pages)
    print(info)
    info2 = "%(title)s, - %(subject)s written by %(author)s has %(pages)d" % dict(title=pdf2.title, subject=pdf2.subject, author=pdf2.author, pages=pdf2.pages)
    print("The text for page 56 follows:")
    print(pdf.getPage(57))
    print("  ")
    print("NEXT PDF")
    print(info2)
    print("The text for page 56 from pdf2 follows:")
    print(pdf2.getPage(57))
    print("And Another Page From the first pdf...")
    print(pdf.getPage(58))