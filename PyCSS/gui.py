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
        _notebook = ttk.Notebook(css_window, height=200)
        _notebook.grid(row=0, column=0, sticky=(E, W, N, S), padx=10)
        tab1 = ttk.Frame(_notebook)
        tab2 = ttk.Frame(_notebook)
        tab3 = ttk.Frame(_notebook)
        entrytext = StringVar()
        entrytext.set('tester')
        entrytest = ttk.Entry(tab1, width=40, textvariable=entrytext)
        entrytest.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)
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
