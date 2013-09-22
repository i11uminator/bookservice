'''
Created on Sep 22, 2013

@author: root
'''

import os

class DirUtils(object):
     
    def listAllInDir(self, path=None):
        if path == None:
            path = os.getcwd()
        lidir = []
        for p in os.listdir(path):
            lidir.append(self.fullName(path, p))
        return lidir
    
    def listAllDirs(self, path=None):
        if path == None:
            path = os.getcwd()
        lidir = []
        for p in os.listdir(path):
            if os.path.isdir(p):
                lidir.append(self.fullName(path, p))
        return lidir
    
    def listAllFiles(self, path=None):
        if path == None:
            path = os.getcwd()
        lidir = []
        for p in os.listdir(path):
            if os.path.isfile(p):
                lidir.append(self.fullName(path, p))
        return lidir
    
    def listAllByExt(self, ext, path=None):
        if path == None:
            path = os.getcwd()
        lidir = []
        for p in os.listdir(path):
            if os.path.basename(p).endswith(ext):
                lidir.append(self.fullName(path, p))
        return lidir
    
    def fullName(self, dir, name):
        return str("%(dirname)s/%(basename)s" % dict(dirname=dir, basename=name))