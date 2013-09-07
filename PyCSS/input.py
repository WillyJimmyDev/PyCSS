#!/usr/bin/python

import glob
import re
import os
from html.parser import HTMLParser

RECURSIVE = True

STOPPARSING = False

html = {}
css = {}
filesnotfound = {}

class MyHTMLParser(HTMLParser):
    
    def __init__(self, afile=None, cssdict=None, **kwds):
        super(MyHTMLParser, self).__init__(**kwds)
        self.afile = afile
        self.cssclasses = cssdict
        self.cssfound = {}
        
    def handle_starttag(self, tag, attrs):
        
        if tag == 'link':
            
            for attr in attrs:
                
                if (attr[0] == 'href'):
                    
                    extension = os.path.splitext(attr[1])[1]
                    if (extension == '.css'):
                    
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
                                
                                ids = re.findall(r'^(#\w+)\s*[^;]{?', line)
                                classes = re.findall(r'^(\.\w+)\s*{?', line)
                                #need to test multiple ids in same line - list should be returned
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
                                
                                csslinenum = csslinenum + 1
                                
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
        if tag == 'head':
            STOPPARSING = True

#userdir = input("Enter a directory to search:\n")
userdir = "/home/elanman/www/"

while not os.path.isdir(userdir):
    print("Can't find the specified directory\nMake sure you entered the path correctly\n")
    userdir = input("Enter a directory to search:\n")

#userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")
userexts = "html"
    
exts = userexts.split(",")

for ext in exts:
    print ("Searching file extension... ", ext)
    
    if RECURSIVE:
        files = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(userdir)
                 for f in files if f.endswith('.' + ext)]
    else:
        files = glob.glob(userdir + "*." + ext)
    
    print("number of files searched:", len(files))
    for file in files:
        
        parser = MyHTMLParser(file, css, strict=False)
        
        filecss = {}
    
        handle = open(file, "r")
        try:
            content = handle.readlines()
            linenum = 1
            cssfound = False
            
            for line in content:
                
                if not STOPPARSING:
                    parser.feed(line)
                    
                classes = re.findall(r'class=\"(.+?)\"', line)
                if classes:
                    cssfound = True
                    for htmlclass in classes:
                        htmlclass = "." + htmlclass
                        filecss[htmlclass] = linenum
                
                ids = re.findall(r'id=\"(.+?)\"', line)
                if ids:
                    cssfound = True
                    for htmlid in ids:
                        htmlid = "#" + htmlid
                        filecss[htmlid] = linenum
                        
                linenum = linenum + 1
              
            if cssfound:
                html[file] = filecss 
        except UnicodeDecodeError as e:
            print(e)

for file in html:
    
    print("processing ...", file)
    used = []
    unused = []
    
    if file in css:
        
        for c,s in css[file].items():
            print("    css file is", c)
            #need to add css file for each used /unused
            for i,l in s["ids"].items():
                
                if i in html[file]:
                    used.append({i:l})
                    
                else:
                    unused.append({i:l})
                    
            for i,l in s["classes"].items():
                
                if i in html[file]:
                    used.append({i:l})
                    
                else:
                    unused.append({i:l})
                  
    if used:
        print("        used css:")
        for l in used:
            for key in l:
                lines = str(l[key]).strip("[]")
                print("            ", key, "on line(s)", lines)
 
    if unused:
        print("        unused css:")
        for l in unused:
            for key in l:
                lines = str(l[key]).strip("[]")
                print("            ", key, "on line(s)", lines)
                
if filesnotfound:
    
    print("Files not found:")
                    
    for l in filesnotfound:
        print("    ",l)
        for files in filesnotfound[l]:
            print("        ",files)