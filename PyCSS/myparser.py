import os
import re
from html.parser import HTMLParser


class PyCSSParser(HTMLParser):

    def error(self, message):
        # should do logging here
        pass

    # dictionary of css files not found and which (html) file they were linked from
    cssfilesnotfound = {}

    # dict of cssclasses
    cssclasses = {}

    cssfound = {}
    
    def __init__(self, afile=None):
        self.html_filename = afile
        super().__init__()

    def handle_starttag(self, tag, attrs):

        if tag != 'link':
            return
            
        for key, value in attrs:

            if key == 'href':

                if '.css' == os.path.splitext(value)[1]:

                    cssfile = os.path.abspath(os.path.join(os.path.dirname(self.html_filename), value))

                    self.cssfound[cssfile] = {'ids': {}, 'classes': {}}
                    idoccurrences = {}
                    classoccurrences = {}

                    try:
                        with open(cssfile, "r") as csshandle:

                            for linenumber, line in enumerate(csshandle.readlines()):

                                linenumber += 1

                                ids = re.findall(r'^(#\w+)\s*[^;]\{?', line)
                                classes = re.findall(r'^(\.\w+)\s*\{?', line)

                                for theid in ids:
                                    if theid not in idoccurrences:
                                        idoccurrences[theid] = [linenumber]
                                    else:
                                        idoccurrences[theid].append(linenumber)
                                for theclass in classes:
                                    if theclass not in classoccurrences:
                                        classoccurrences[theclass] = [linenumber]
                                    else:
                                        classoccurrences[theclass].append(linenumber)

                        self.cssfound[cssfile]["ids"] = idoccurrences
                        self.cssfound[cssfile]["classes"] = classoccurrences

                    except (OSError, IOError):
                        if self.html_filename in self.cssfilesnotfound:
                            self.cssfilesnotfound[self.html_filename].append(cssfile)
                        else:
                            self.cssfilesnotfound[self.html_filename] = [cssfile]
        
        self.cssclasses[self.html_filename] = self.cssfound

