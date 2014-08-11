import os
import re
from html.parser import HTMLParser

# dictionary of css files not found and which (html) file they were linked from
filesnotfound = {}

#dictionary of all classes and ids found in linked css files
css = {}


class MyHTMLParser(HTMLParser):
    
    def __init__(self, afile=None, cssdict=None, **kwds):
        super(MyHTMLParser, self).__init__(**kwds)
        self.afile = afile
        self.cssclasses = cssdict
        self.cssfound = {}
        
    def handle_starttag(self, tag, attrs):
        
        if tag == 'link':
            
            for attr in attrs:
                
                if attr[0] == 'href':
                    
                    extension = os.path.splitext(attr[1])[1]
                    if extension == '.css':
                    
                        newfile = os.path.join(os.path.dirname(self.afile), attr[1])

                        cssfile = os.path.abspath(newfile)
                        
                        self.cssfound[cssfile] = {}
                        
                        try:
                            self.cssfound[cssfile]["ids"] = {}
                            self.cssfound[cssfile]["classes"] = {}
                            idoccurrences = {}
                            classoccurrences = {}
                            
                            csshandle = open(cssfile, "r")
                            csscontent = csshandle.readlines()
                            csslinenum = 1
                            for line in csscontent:
                                
                                ids = re.findall(r'^(#\w+)\s*[^;]\{?', line)
                                classes = re.findall(r'^(\.\w+)\s*\{?', line)
                                
                                for theid in ids:
                                    if theid not in idoccurrences:
                                        idoccurrences[theid] = []
                                        idoccurrences[theid].append(csslinenum)
                                    else:
                                        idoccurrences[theid].append(csslinenum)
                                for theclass in classes:
                                    if theclass not in classoccurrences:
                                        classoccurrences[theclass] = []
                                        classoccurrences[theclass].append(csslinenum)
                                    else:
                                        classoccurrences[theclass].append(csslinenum)
                                
                                csslinenum += 1
                                
                            self.cssfound[cssfile]["ids"] = idoccurrences
                            self.cssfound[cssfile]["classes"] = classoccurrences
                            
                        except (OSError, IOError):
                            if self.afile in filesnotfound:
                                filesnotfound[self.afile].append(cssfile)
                            else:
                                filesnotfound[self.afile] = []
                                filesnotfound[self.afile].append(cssfile)
        
        if self.cssfound:                            
            css[self.afile] = self.cssfound
        
        return css
                                    
    def handle_endtag(self, tag):
        global STOPPARSING
        if tag == 'head':
            STOPPARSING = True