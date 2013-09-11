#!/usr/bin/python

import glob
import re
import os
from myparser import MyHTMLParser, filesnotfound, css

# by default, the file search is performed recursively
RECURSIVE = True

# set to True when we reach the end of the <head> section no more css files to find?
STOPPARSING = False

#dictionary of all html classes and ids found in (html) files
html = {}

#list of all (html) files found not in the 'correct' encoding (utf-8)
encodingerrors = []

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
    
    print("number of files found:", len(files))
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
                 
        except UnicodeDecodeError:
            if not file in encodingerrors:
                encodingerrors.append(file)

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

if encodingerrors:
    print("Files found with encoding errors (not utf-8): ")
    for f in encodingerrors:
        print(f)