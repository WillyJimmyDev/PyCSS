#!/usr/bin/python

import glob
import re
import os
from html.parser import HTMLParser


linkedcss = []


htmlclasses = []
htmlids = []
cssclasses = []
cssids = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        
        if (tag == 'link'):
            
            for attr in attrs:
                
                if (attr[0] == 'href'):
                    
                    extension = os.path.splitext(attr[1])[1]
                    if (extension == '.css'):
                        
                        cssfile = os.path.abspath((userdir + attr[1]))
                        linkedcss.append(cssfile)
                        
                        csshandle = open(cssfile, "r")
                        csscontent = csshandle.readlines()
                        for line in csscontent:
                            words = line.split()
                            for word in words:
                                if word.startswith("."):
                                    print (word)
                                    cssclasses.append(word)
                                    
                                if word.startswith("#"):
                                    print (word)
                                    cssids.append(word)

userdir = input("Enter a directory to search\n")
userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")

parser = MyHTMLParser(strict=False)

exts = userexts.split(",")

for ext in exts:
    print ("current file extension is ", ext)

    files = glob.glob(userdir + "*." + ext)
    print("number of files searched", len(files))
    for file in files:
        
        print("current file name is ", file)
        handle = open(file, "r")
        content = handle.readlines()
        linenum = 0
        classfound = False
        idfound = False
        
        for line in content:
            parser.feed(line)
            classes = re.findall(r'class=\"(.+?)\"', line)
            if classes:
                classfound = True
                for htmlclass in classes:
                    print(" class found -> .", htmlclass, " on line ", linenum, sep='')
                    htmlclasses.append(htmlclass)
            
            ids = re.findall(r'id=\"(.+?)\"', line)
            if ids:
                idfound = True
                for htmlid in ids:
                    print(" id found -> #", htmlid, " on line ", linenum,sep='')
                    htmlids.append(htmlid)
                    
            linenum = linenum + 1
            
        if not classfound:
            print("no classes found in file")
            
        if not idfound:
            print("no ids found in file")

print(linkedcss)
print("html class list is ", htmlclasses)
print("html id list is ", htmlids)
print("css class list is ", cssclasses)
print("css id list is ", cssids)
#need multi-demensional array to hold filename, line number of occurrence ,class name, id name etc
