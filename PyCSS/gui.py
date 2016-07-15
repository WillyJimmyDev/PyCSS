from tkinter import *
from tkinter import ttk, filedialog
import os


class Gui:

    def __init__(self, _root):
        self._root = _root

    def show_css_details(self, _menubar, *args):
        css_window = Toplevel(self._root)
        css_window['menu'] = _menubar
        css_window.title('Css Details')
        css_window.geometry('500x500')
        ttk.Sizegrip(css_window).pack(side='bottom', anchor='se')
        _notebook = ttk.Notebook(css_window)
        _notebook.pack(fill='both', expand='yes', ipadx=5)
        tab1 = ttk.Frame(_notebook)
        tab2 = ttk.Frame(_notebook)
        tab3 = ttk.Frame(_notebook)

        _used_files = StringVar()
        _unused_files = StringVar()
        _general_info = StringVar()

        formatted_used = self._format_css_info(args[1])
        formatted_unused = self._format_css_info(args[2])

        _general_info.set(args[0])
        _used_files.set(formatted_used)
        _unused_files.set(formatted_unused)

        _general_listbox = Listbox(tab1, exportselection=0, listvariable=_general_info)
        _general_listbox.pack(fill='both', expand='yes', ipadx=5)

        _used_css_listbox = Listbox(tab2, exportselection=0, listvariable=_used_files)
        _used_css_listbox.pack(fill='both', expand='yes', ipadx=5)

        _unused_css_listbox = Listbox(tab3, exportselection=0, listvariable=_unused_files)
        _unused_css_listbox.pack(fill='both', expand='yes', ipadx=5)

        _notebook.add(tab1, text='General')
        _notebook.add(tab2, text='Used CSS')
        _notebook.add(tab3, text='Redundant CSS')

    @staticmethod
    def get_directory(directory):
        home = os.path.expanduser('~')
        selected_dir = filedialog.askdirectory(initialdir=home)
        if selected_dir:
            directory.set(selected_dir)

    def show_about_window(self, *args):
        about_window = Toplevel(self._root)
        about_window.title('About PyCSS')
        about_window.geometry('500x500')

    @staticmethod
    def _format_css_info(cssinfo):

        formatted = []
        for l in cssinfo:
            for key in l:
                formatted.append(str("{} on line(s) {}".format(key, str(l[key]).strip('[]'))))

        return formatted

        # if self.cssfilesnotfound:
        #     # populate a 'not found tab on interface'
        #     print("Files not found:")
        #
        #     for l in self.cssfilesnotfound:
        #         print("    HTML File: ", l)
        #         print("        CSS Files Linked From HTML:")
        #         for file in self.cssfilesnotfound[l]:
        #             print("        ", file)
        #
        # if self.encodingerrors:
        #     # populate an 'encoding errors tab in interface'
        #     print("Files found with encoding errors (not utf-8): ")
        #     for f in self.encodingerrors:
        #         print(f)
