import glob
import re
import os
from myparser import MyHTMLParser

# by default, the file search is performed recursively
RECURSIVE = True

# dictionary of all html classes and ids found in (html) files
html = {}

# list of all (html) files found not in the 'correct' encoding (utf-8)
encodingerrors = []

# get the directory to traverse from user input
userdir = input("Enter a directory to search:\n")

# if we can't find the directory, prompt the user for another
while not os.path.isdir(userdir):
    print("Can't find the specified directory\nMake sure you entered the path correctly\n")
    userdir = input("Enter a directory to search:\n")

for ext in ["shtml", "html", "xhtml"]:
    print("Searching file extension... ", ext)

    # recursive search of user directory or not
    if RECURSIVE:
        files = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(userdir)
                 for f in files if f.endswith('.' + ext)]
    else:
        files = glob.glob(userdir + "*." + ext)

    print("number of files found:", len(files))
    for file in files:

        parser = MyHTMLParser(file)

        filecss = {}

        handle = open(file, "r")
        try:
            content = handle.readlines()
            linenum = 1
            cssfound = False

            for line in content:

                if not parser.stopparsing:
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

                linenum += 1

            if cssfound:
                html[file] = filecss

        except UnicodeDecodeError:
            if file not in encodingerrors:
                encodingerrors.append(file)

if html:
    for file in html:

        print("processing ...", file)

        if file in parser.cssclasses:

            for c, s in parser.cssclasses[file].items():

                used = []
                unused = []

                # l is the list of line numbers
                for i, l in s["ids"].items():

                    if i in html[file]:
                        used.append({i: l})

                    else:
                        unused.append({i: l})

                for i, l in s["classes"].items():

                    if i in html[file]:
                        used.append({i: l})

                    else:
                        unused.append({i: l})

                if used or unused:
                    print("    searching css file:", c)

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

if parser.filesnotfound:

    print("Files not found:")

    for l in parser.filesnotfound:
        print("    HTML File: ", l)
        print("        CSS Files Linked From HTML:")
        for file in parser.filesnotfound[l]:
            print("        ", file)

if encodingerrors:
    print("Files found with encoding errors (not utf-8): ")
    for f in encodingerrors:
        print(f)