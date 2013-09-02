#!/usr/bin/python

import os
import glob
import re

holder = []

userdir = input("Enter a directory to search\n")
userexts = input("Enter a comma separated list of file extensions to search in e.g php,html\n")

print(userexts)
exts = userexts.split(",")

for ext in exts:
    print ("current file extension is ", ext)

    files = glob.glob(userdir + "*." + ext)

    for file in files:
        
        print("current file name is ", file)
        handle = open(file, "r")
        content = handle.readlines()
        linenum = 0
        
        for line in content:

            classes = re.findall(r'class=\"(.+?)\"', line)
            if classes:
                for cssclass in classes:
                    print(" class found: ", cssclass, "on line ", linenum)
                    holder.append(cssclass)
            
            linenum = linenum + 1

# holder now holds all classes mentioned in the files
print(holder)

#need multi-demensional array to hold filename, line number of occurrence ,class name, id name etc
#need a separate loop for ids
#need a list of all css files linked to from file
