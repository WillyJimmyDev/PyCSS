#!/usr/bin/python

import glob
import re
import os
from html.parser import HTMLParser

stopparsing = False

html = {}
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
                
                if (attr[0] == 'href'):
                    
                    extension = os.path.splitext(attr[1])[1]
                    if (extension == '.css'):
                        
                        cssfile = os.path.abspath((userdir + attr[1]))
                        
                        self.cssfound[cssfile] = {}
                        
                        csshandle = open(cssfile, "r")
                        csscontent = csshandle.readlines()
                        csslinenum = 0
                        for line in csscontent:
                            
                            words = line.split()
                            for word in words:
                                if word.startswith(".") or word.startswith("#"):
                                    self.cssfound[cssfile][word] = csslinenum
                            
                            csslinenum = csslinenum + 1
        
        if self.cssfound:                            
            css[self.afile] = self.cssfound
        
        return css
                                    
    def handle_endtag(self, tag):
        if tag == 'head':
            stopparsing = True

userdir = input("Enter a directory to search\n")
userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")

exts = userexts.split(",")

for ext in exts:
    print ("Searching file extension... ", ext)

    files = glob.glob(userdir + "*." + ext)
    print("number of files searched:", len(files))
    for file in files:
        
        parser = MyHTMLParser(file, css, strict=False)
        
        filecss = {}
    
        handle = open(file, "r")
        content = handle.readlines()
        linenum = 0
        cssfound = False
        
        for line in content:
            
            if not stopparsing:
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
            
print("html list is ", set(html.keys()))
print("css list is ", set(css.keys()))

print(html)
print("dict of files with linked css files and classes/line numbers therein", css)

for fileid,cssitems in css.items():
    print("    The file is",fileid)
    # loop through the html file ids and classes here
    for k,v in cssitems.items():
        print("        linked css file is .",k, sep='')
        for c,l in v.items():
            print("            css is ",c, " found on line ", l, sep='')
        
htmlfiles = set(html.keys())
cssfiles = set(css.keys())
combinedfiles = cssfiles.intersection(htmlfiles)
print("in both", combinedfiles)