#!/usr/bin/python

import glob
import re
import os
from html.parser import HTMLParser

stopparsing = False

linkedcss = []


htmlclasses = []
htmlids = {}
cssclasses = []
cssids = []

linkedfiles = {}

class MyHTMLParser(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        
        if tag == 'link':
            
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
                                    cssclasses.append(word)
                                    
                                if word.startswith("#"):
                                    cssids.append(word)
                                    
    def handle_endtag(self, tag):
        if tag == 'head':
            #print("end tag is",tag)
            stopparsing = True

userdir = input("Enter a directory to search\n")
userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")

parser = MyHTMLParser(strict=False)

exts = userexts.split(",")

for ext in exts:
    print ("Searching file extension... ", ext)

    files = glob.glob(userdir + "*." + ext)
    print("number of files searched:", len(files))
    for file in files:
        
        fileids = {}
    
        handle = open(file, "r")
        content = handle.readlines()
        linenum = 0
        classfound = False
        idfound = False
        
        for line in content:
            
            if not stopparsing:
                parser.feed(line)
            classes = re.findall(r'class=\"(.+?)\"', line)
            if classes:
                classfound = True
                for htmlclass in classes:
                    htmlclasses.append(htmlclass)
            
            ids = re.findall(r'id=\"(.+?)\"', line)
            if ids:
                idfound = True
                for htmlid in ids:
                    fileids[htmlid] = linenum
                    
            linenum = linenum + 1
            
        #if not classfound:
            #print("no classes found in file")
          
        if idfound:
            htmlids[file] = fileids  
        #else:
            #print("no ids found in file")
        
#print(linkedcss)
#print("html class list is ", htmlclasses)
#print("html id list is ", htmlids)
print("number of files with ids in", len(htmlids))
for fileid,ids in htmlids.items():
    print("    The file is",fileid)
    for k,v in ids.items():
        print("        ID is #",k," on line ",v,sep='')
#print("css class list is ", cssclasses)
#print("css id list is ", cssids)
#need multi-demensional array to hold html filename, linked css file, line numbers of occurrences ,class name, id name etc
