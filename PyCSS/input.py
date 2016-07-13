import glob
import re
import os
from myparser import PyCSSParser

# from tkinter import *
# from tkinter import ttk, filedialog, messagebox
#
# _root = Tk()
# _root.title('PyCSS')
# _mainframe = ttk.Frame(_root, padding='5 5 5 5')
# _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))
#
# _directory_frame = ttk.LabelFrame(_mainframe, text='Directory', padding='5 5 5 5')
# _directory_frame.grid(row=0, column=0, sticky=(E, W))
# _directory_frame.columnconfigure(0, weight=1)
# _directory_frame.rowconfigure(0, weight=1)
#
# _directory = StringVar()
# _directory.set(os.path.expanduser('~/www'))
# _directory_entry = ttk.Entry(_directory_frame, width=40, textvariable=_directory)
# _directory_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)
# _fetch_btn = ttk.Button(_directory_frame, text='Fetch CSS information')
# _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)
#
# _img_frame = ttk.LabelFrame(_mainframe, text='Files', padding='9 0 0 0')
# _img_frame.grid(row=1, column=0, sticky=(N, S, E, W))
#
# _images = StringVar()
# _img_listbox = Listbox(_img_frame, listvariable=_images, height=6, width=25)
# _img_listbox.grid(row=0, column=0, sticky=(E, W), pady=5)
# _scrollbar = ttk.Scrollbar(_img_frame, orient=VERTICAL, command=_img_listbox.yview)
# _scrollbar.grid(row=0, column=1, sticky=(S, N), pady=6)
# _img_listbox.configure(yscrollcommand=_scrollbar.set)
# _radio_frame = ttk.Frame(_img_frame)
# _radio_frame.grid(row=0, column=2, sticky=(N, S, W, E))
# _choice_lbl = ttk.Label(_radio_frame, text="Choose which file extensions to parse")
# _choice_lbl.grid(row=0, column=0, padx=5, pady=5)
# _save_method = StringVar()
# _save_method.set('img')
# _img_only_radio = ttk.Radiobutton(_radio_frame, text='.html', variable=_save_method, value='img')
# _img_only_radio.grid(row=1, column=0, padx=5, pady=2, sticky=W)
# _img_only_radio.configure(state='normal')
# _json_radio = ttk.Radiobutton(_radio_frame, text='.php', variable=_save_method, value='json')
# _json_radio.grid(row=2, column=0, padx=5, pady=2, sticky=W)
# _scrape_btn = ttk.Button(_mainframe, text='Parse CSS!')
# _scrape_btn.grid(row=2, column=0, sticky=E, pady=5)
# _status_frame = ttk.Frame(_root, relief='sunken', padding='2 2 2 2')
# _status_frame.grid(row=1, column=0, sticky=(E, W, S))
# _status_msg = StringVar()
# _status_msg.set('Enter a directory to search:')
# _status = ttk.Label(_status_frame, textvariable=_status_msg, anchor=W)
# _status.grid(row=0, column=0, sticky=(E, W))
# _root.mainloop()
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

        parser = PyCSSParser(file)

        filecss = {}

        try:
            cssfound = False

            with open(file, "r") as handle:

                linenum = 1
                for line in handle.readlines():

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
                print(s)
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
                    print(used)
                    print(unused)

                if used:
                    print("        used css:")
                    for l in used:
                        for key in l:
                            lines = l[key]
                            print("            ", key, "on line(s)", *lines)

                if unused:
                    print("        unused css:")
                    for l in unused:
                        for key in l:
                            lines = l[key]
                            print("            ", key, "on line(s)", *lines)

if parser.cssfilesnotfound:

    print("Files not found:")

    for l in parser.cssfilesnotfound:
        print("    HTML File: ", l)
        print("        CSS Files Linked From HTML:")
        for file in parser.cssfilesnotfound[l]:
            print("        ", file)

if encodingerrors:
    print("Files found with encoding errors (not utf-8): ")
    for f in encodingerrors:
        print(f)
