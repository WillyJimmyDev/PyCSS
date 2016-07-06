import os
import re
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def error(self, message):
        pass
    
    def __init__(self, afile=None, **kwds):
        super().__init__(**kwds)
        self.afile = afile
        self.cssfound = {}
        # set to True when we reach the end of the <head> section no more css files to find?
        self.stopparsing = False

        # dictionary of css files not found and which (html) file they were linked from
        self.filesnotfound = {}

        # dict of cssclasses
        self.cssclasses = {}
        
    def handle_starttag(self, tag, attrs):

        if tag != 'link':
            return
            
        for attr in attrs:

            if attr[0] == 'href':

                extension = os.path.splitext(attr[1])[1]
                if extension == '.css':

                    newfile = os.path.join(os.path.dirname(self.afile), attr[1])

                    cssfile = os.path.abspath(newfile)

                    self.cssfound[cssfile] = {'ids': {}, 'classes': {}}
                    idoccurrences = {}
                    classoccurrences = {}

                    try:
                        with open(cssfile, "r") as csshandle:
                            csslinenum = 1
                            for line in csshandle.readlines():

                                ids = re.findall(r'^(#\w+)\s*[^;]\{?', line)
                                classes = re.findall(r'^(\.\w+)\s*\{?', line)

                                for theid in ids:
                                    if theid not in idoccurrences:
                                        idoccurrences[theid] = [csslinenum]
                                    else:
                                        idoccurrences[theid].append(csslinenum)
                                for theclass in classes:
                                    if theclass not in classoccurrences:
                                        classoccurrences[theclass] = [csslinenum]
                                    else:
                                        classoccurrences[theclass].append(csslinenum)

                                csslinenum += 1

                            self.cssfound[cssfile]["ids"] = idoccurrences
                            self.cssfound[cssfile]["classes"] = classoccurrences

                    except (OSError, IOError):
                        if self.afile in self.filesnotfound:
                            self.filesnotfound[self.afile].append(cssfile)
                        else:
                            self.filesnotfound[self.afile] = [cssfile]

        self.cssclasses[self.afile] = self.cssfound
        
        return self.cssclasses
                                    
    def handle_endtag(self, tag):

        if tag == 'head':
            self.stopparsing = True
