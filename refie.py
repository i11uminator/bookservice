import web
import xml.etree.ElementTree as ET
import subprocess
import uuid
import os

urls = ( 
	    '/books', 'bypage',
	    '/books/pages', 'page',
	    '/books/getpage/([0-9]*)', 'getpage'
	)

class wserver(web.application):
    def run(self, port=8080, *middleware):
	func = self.wsgifunc(*middleware)
	return web.httpserver.runsimple(func, ('0.0.0.0', port))

class bypage:
    def GET(self):
	return "<form method='POST' action='bypage'>First Page:<input type='text' name='first'><br>Last Page:<input type='text' name='last'><input type='submit' value='submit'></form>"

    def POST(self):
	params = web.input()
	p = PdfHtml('/home/brad/Documents/Books/Linux/Learning_The_Bash_Shell_Third_Edition.pdf')
	return p.htmlpage(110, 110)

class page:
    def GET(self):
	p = PdfHtml('/home/brad/Documents/Books/Linux/Learning_The_Bash_Shell_Third_Edition.pdf')
	return p.htmlpage(110, 110)

class getpage:
    def GET(self, page):
	p = PdfHtml('/home/brad/Documents/Books/Linux/Learning_The_Bash_Shell_Third_Edition.pdf')
	return p.htmlpage(page, page)

class PdfHtml(object):
    filename = None

    def __init__(self, filename):
	self.filename = filename
	
    def htmlpage(self, first, last):
	''' return html '''
	tmp = "/tmp"
	guid = str(uuid.uuid1())
	# convert the file with a random name into temp dir
	command = "pdftohtml -f %s -l %s -q -noframes -stdout -nodrm %s" % (first, last, self.filename)
	#p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=os.path.join(settings.PROJECT_DIR, "website/templates"))
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	# now find the file and read it into a string
	error = p.stderr.readlines()
	if error:
	    raise Exception("".join(error))
	html = p.stdout.readlines()
	return "".join(html)	

if __name__ == "__main__":
    app = wserver(urls, globals())
    app.run(9999)
			
