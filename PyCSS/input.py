#!/usr/bin/python

import glob
import re

classholder = []
idholder = []

userdir = input("Enter a directory to search\n")
userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")

print(userexts)
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

            classes = re.findall(r'class=\"(.+?)\"', line)
            if classes:
                classfound = True
                for cssclass in classes:
                    print(" class found -> .", cssclass, " on line ", linenum, sep='')
                    classholder.append(cssclass)
            
            ids = re.findall(r'id=\"(.+?)\"', line)
            if ids:
                idfound = True
                for cssid in ids:
                    print(" id found -> #", cssid, " on line ", linenum,sep='')
                    idholder.append(cssid)
                    
            linenum = linenum + 1
            
        if not classfound:
            print("no classes found in file")
            
        if not idfound:
            print("no ids found in file")

# holder now holds all classes mentioned in the files
print("class list is ", classholder)
print("id list is ", idholder)

#need multi-demensional array to hold filename, line number of occurrence ,class name, id name etc
#need a list of all css files linked to from file
