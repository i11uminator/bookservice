'''
Created on Sep 22, 2013

@author: root
'''

class ListUtils(object):
    
    def AnyObjectInListHas(self, alist, func, **kwargs):
        for x in alist:
            if kwargs:
                if func(x, kwargs):
                    return True
            else:
                if func(x):
                    return True
        return False

    def NObjectsInListHave(self, alist, func, **kwargs):
        n = 0
        for x in alist:
            if kwargs:
                if func(x, kwargs):
                    n = n + 1
            else:
                if func(x):
                    n = n + 1
        return n 