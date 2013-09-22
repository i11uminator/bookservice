'''
Created on Sep 22, 2013

@author: root
'''

import web

class wserver(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))