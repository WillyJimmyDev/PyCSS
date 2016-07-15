import argparse
import glob
import os
import copy
from tkinter import *
from tkinter import ttk, messagebox

from myparser import PyCSSParser
from gui import Gui


class PyCSS:

    def __init__(self, master):
        self.gui = Gui(master)
        self.encodingerrors = []
        self.fetched_files = []
        self.used = []
        self.unused = []
        self.cssclasses = {}
        self.cssfilesnotfound = {}
        self.css_selectors = {}

    @staticmethod
    def update_status_bar(*args):
        _css_files.set(())
        selected_file = _file_listbox.get(_file_listbox.curselection())
        if selected_file:
            _status_msg.set(selected_file)

    def show_about_window(self, *args):
        self.gui.show_about_window(*args)

    def show_css_details(self, *args):
        selected_css_file = _css_listbox.get(_css_listbox.curselection())
        if selected_css_file:
            details = [selected_css_file, self.used, self.unused]
            self.gui.show_css_details(_menubar, *details)

    def get_directory(self):
        self.gui.get_directory(_directory)

    def fetch_files(self, recursive_search=True):
        directory = _directory.get()
        if not directory:
            messagebox.showerror('No Directory Selected', 'Please select a directory', icon='error')
            return
        _files.set(())
        self.fetched_files[:] = []
        for ext in ["shtml", "html", "xhtml"]:

            if recursive_search:
                files = [os.path.join(dirpath, f)
                         for dirpath, dirnames, files in os.walk(directory)
                         for f in files if f.endswith('.' + ext)]
            else:
                files = glob.glob(directory + "*." + ext)

            self.fetched_files += files

        _files.set(self.fetched_files)
        _status_msg.set('Search results for {}'.format(directory) if self.fetched_files else 'No files found')

    def parse_file(self, *args):
        self.css_selectors.clear()
        self.encodingerrors[:] = []
        self.cssclasses.clear()
        self.cssfilesnotfound.clear()

        file = self.fetched_files[_file_listbox.curselection()[0]]
        parser = PyCSSParser(file)

        try:

            with open(file, "r") as handle:

                for linenum, line in enumerate(handle.readlines()):

                    linenum += 1

                    parser.feed(line)  # parser looks for classes and ids in linked css files

                    classes = re.findall(r'class=\"(.+?)\"', line)
                    if classes:
                        for html_class in classes:
                            html_class = "." + html_class
                            self.css_selectors[html_class] = linenum

                    ids = re.findall(r'id=\"(.+?)\"', line)
                    if ids:
                        for html_id in ids:
                            html_id = "#" + html_id
                            self.css_selectors[html_id] = linenum

                handle.close()

        except UnicodeDecodeError:
            if file not in self.encodingerrors:
                self.encodingerrors.append(file)

        self.cssclasses, self.cssfilesnotfound = copy.deepcopy(parser.cssclasses), copy.deepcopy(parser.cssfilesnotfound)
        self._link_css_ids_and_classes(file)

    def _link_css_ids_and_classes(self, html_file):
        self.used[:] = []  # reset the class lists
        self.unused[:] = []  # reset the class lists

        if html_file in self.cssclasses:

            for cssfile, css in self.cssclasses[html_file].items():

                # l is the list of line numbers
                for _id, linenumbers in css["ids"].items():

                    if _id in self.css_selectors:
                        self.used.append({_id: linenumbers})
                    else:
                        self.unused.append({_id: linenumbers})

                for _class, linenumbers in css["classes"].items():

                    if _class in self.css_selectors:
                        self.used.append({_class: linenumbers})
                    else:
                        self.unused.append({_class: linenumbers})

                if self.used or self.unused:
                    _css_files.set(cssfile)

                self._output_css_info()
        else:
            print('no linked css files found')

    def _output_css_info(self):

        if self.used:
            for l in self.used:
                for key in l:
                    lines = l[key]
                    print("            ", key, "on line(s)", *lines)

        if self.unused:
            for l in self.unused:
                for key in l:
                    lines = l[key]
                    print("            ", key, "on line(s)", *lines)

        if self.cssfilesnotfound:
            # populate a 'not found tab on interface'
            print("Files not found:")

            for l in self.cssfilesnotfound:
                print("    HTML File: ", l)
                print("        CSS Files Linked From HTML:")
                for file in self.cssfilesnotfound[l]:
                    print("        ", file)

        if self.encodingerrors:
            # populate an 'encoding errors tab in interface'
            print("Files found with encoding errors (not utf-8): ")
            for f in self.encodingerrors:
                print(f)


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description='Check For Unused CSS Styles.')
    argparser.add_argument(
        '-t',
        '--type',
        choices=['all', 'html', 'shtml', 'xhtml'],
        default='all',
        help='The file types we wish to check.')
    argparser.add_argument(
        'directory',
        help='The directory we wish to search inside.')
    args = argparser.parse_args()

    _root = Tk()
    pycss = PyCSS(_root)
    _root.option_add('*tearOff', FALSE)
    _root.title('PyCSS')
    _root.columnconfigure(0, weight=1)
    _root.rowconfigure(0, weight=1)
    ttk.Sizegrip(_root).grid(column=999, row=999, sticky=(S, E))
    _menubar = Menu(_root)

    _menu_file = Menu(_menubar)
    _menu_about = Menu(_menubar)
    _menu_help = Menu(_menubar, name='help')
    _menubar.add_cascade(menu=_menu_file, label='File')
    _menubar.add_cascade(menu=_menu_about, label='About')
    _menubar.add_cascade(menu=_menu_help, label='Help')
    _menu_file.add_command(label='Close', command=pycss.parse_file)
    _menu_about.add_command(label='PyCSS Licence', command=pycss.show_about_window)
    _root['menu'] = _menubar

    _mainframe = ttk.Frame(_root, padding='5 5 5 5')
    _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))
    _mainframe.columnconfigure(0, weight=1)
    _mainframe.rowconfigure(0, weight=2)
    _mainframe.rowconfigure(1, weight=1)

    _directory_frame = ttk.LabelFrame(_mainframe, text='Directory', padding='5 5 5 5')
    _directory_frame.grid(row=0, column=0, sticky=(E, W, N))
    # _directory_frame.columnconfigure(1, weight=1)
    _directory_frame.columnconfigure(2, weight=1)

    _directory = StringVar()
    _directory.set(args.directory)
    _directory_entry = ttk.Entry(_directory_frame, width=30, textvariable=_directory)
    _directory_entry.grid(row=0, column=0, sticky=(W, N), padx=5, pady=5)
    _directory_entry.bind('<Return>', pycss.fetch_files)

    _directory_btn = ttk.Button(_directory_frame, text='Browse', command=pycss.get_directory)
    _directory_btn.grid(row=0, column=1, sticky=(W, N), padx=5)

    _fetch_btn = ttk.Button(_directory_frame, text='Fetch Files', command=pycss.fetch_files)
    _fetch_btn.grid(row=0, column=2, sticky=(W, N), padx=5)

    # _radio_frame = ttk.Frame(_mainframe)
    # _radio_frame.grid(row=1, column=0, sticky=(N, S, W, E))
    # _choice_lbl = ttk.Label(_radio_frame, text="Choose which file extensions to parse")
    # _choice_lbl.grid(row=0, column=0, padx=5, pady=5)
    # _file_type = StringVar()
    # _file_type.set('html')
    # _html_radio = ttk.Radiobutton(_radio_frame, text='.html', variable=_file_type, value='html')
    # _html_radio.grid(row=1, column=0, padx=5, pady=2, sticky=W)
    # _html_radio.configure(state='normal')
    # _shtml_radio = ttk.Radiobutton(_radio_frame, text='.shtml', variable=_file_type, value='shtml')
    # _shtml_radio.grid(row=2, column=0, padx=5, pady=2, sticky=W)
    # _xhtml_radio = ttk.Radiobutton(_radio_frame, text='.xhtml', variable=_file_type, value='xhtml')
    # _xhtml_radio.grid(row=3, column=0, padx=5, pady=2, sticky=W)
    # _php_radio = ttk.Radiobutton(_radio_frame, text='.php', variable=_file_type, value='php')
    # _php_radio.grid(row=4, column=0, padx=5, pady=2, sticky=W)

    _file_frame = ttk.LabelFrame(_mainframe, text='Files', padding='9 0 0 0')
    _file_frame.grid(row=2, column=0, sticky=(N, S, E, W))
    _file_frame.columnconfigure(0, weight=1)
    _file_frame.rowconfigure(0, weight=1)

    _files = StringVar()
    _file_listbox = Listbox(_file_frame, exportselection=0, listvariable=_files)
    _file_listbox.grid(row=0, column=0, sticky=(N, E, W, S), pady=5)
    # _file_listbox.rowconfigure(0, weight=1)
    # _file_listbox.columnconfigure(0, weight=1)
    _file_listbox.bind('<Double-1>', pycss.parse_file)
    _file_listbox.bind('<Return>', pycss.parse_file)
    _file_listbox.bind('<<ListboxSelect>>', pycss.update_status_bar)

    _css_frame = ttk.LabelFrame(_mainframe, text='Linked CSS Files', padding='9 0 0 0')
    _css_frame.grid(row=3, column=0, sticky=(N, S, E, W))
    _css_frame.columnconfigure(0, weight=1)
    _css_frame.rowconfigure(0, weight=1)
    _css_files = StringVar()

    _css_listbox = Listbox(_css_frame, exportselection=0, listvariable=_css_files)
    _css_listbox.grid(row=0, column=0, sticky=(N, E, W, S), pady=5)
    # _css_listbox.rowconfigure(0, weight=1)
    # _css_listbox.columnconfigure(0, weight=1)
    _css_listbox.bind('<Double-1>', pycss.show_css_details)
    _css_listbox.bind('<Return>', pycss.show_css_details)

    _scrollbar = ttk.Scrollbar(_file_frame, orient=VERTICAL, command=_file_listbox.yview)
    _scrollbar.grid(row=0, column=1, sticky=(S, N), pady=6)
    _file_listbox.configure(yscrollcommand=_scrollbar.set)

    _scrape_btn = ttk.Button(_mainframe, text='Parse CSS!')
    _scrape_btn.grid(row=4, column=0, sticky=E, pady=5)
    _status_frame = ttk.Frame(_root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=(E, W, S))
    _status_msg = StringVar()
    _status_msg.set('Enter a directory to search:')
    _status = ttk.Label(_status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    _root.mainloop()
