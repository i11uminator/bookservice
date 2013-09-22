'''
Created on Sep 22, 2013

@author: root
'''

class StringUtils(object):
    
    def replaceNthOccurance(self, str, old, replace, occurance):
        if occurance <= 0:
            return str
        li = str.split(old, occurance)
        if len(li) < occurance + 1:
            return str
        replaced = old.join(li[:-1]) + replace + li[-1]
        return replaced
    
            
    def findAllOccurances(self, text, tag):
        tags = []
        start = 0
        while text:
            idx = text.find(tag)
            if idx > -1:
                tags.append(idx + start)
                start = start + idx + len(tag)
                text = text[idx + len(tag):]
            else:
                text = ""
        return tags
    
    def rreplace(self, str, old, new, times):
        li = str.rsplit(old, times)
        return new.join(li)