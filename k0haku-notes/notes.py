import enum
import tkinter as tk
import os
from tkinter import ttk
from stuff import ViewRefs

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_NOTES_PATH = ROOT_DIR + '\\data\\notes\\'


def create_popup(title='Popup', msg='', buttons=('OK',)):
    popup = tk.Toplevel()
    popup.title(title)
    label = ttk.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)
    for b in buttons:
        B1 = ttk.Button(popup, text=b, command=popup.destroy)
        B1.pack()

# We don't need obserables, tkinter already has the Variables class 
# that can .trace_add that should work the same, needs testing first
# still might need a model class where we define the logic that can be done on those Variables

# TODO: create a class extending or using the variable class from tkinter that exposes certain fields or whatever
# probably just mimic what you did in the backend


class NotesApp2(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notes_path = tk.StringVar(self, DEFAULT_NOTES_PATH)
        self.selected_node = tk.StringVar(self)  # TODO: do list of selected notes

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._create_menubar()

        self.frames = {}
        frame_list = (ViewRefs.START, ViewRefs.NOTES_OVERVIEW)
        for Frame in frame_list:
            frame_instance = Frame(self.container, self)
            self.frames[Frame] = frame_instance
            frame_instance.grid(row=0, column=0, sticky='nsew')

        self.show_frame(ViewRefs.START)

    def _create_menubar(self):
        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Add file...', command=lambda: create_popup())
        filemenu.add_command(label='Settings', command=lambda: print('lul'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        test = tk.Menu(menubar, tearoff=0)
        test.add_command(label='Exit', command=quit)
        test.add_checkbutton(label='check')
        test.add_separator()
        test.add_radiobutton(label='radio')
        test.add_radiobutton(label='radio2')
        filemenu.add_cascade(label='TEST', menu=test)
        menubar.add_cascade(label='Stuff...', menu=filemenu)

        self.config(menu=menubar)

    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if frame is not None:
            frame.destroy()
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames[cont] = frame

    def get_file_path(self):
        return self.notes_path.get() + self.selected_node.get()


def print_text(text):
    print(text)

# app = NotesApp()
# app.geometry('640x480')
# app.mainloop()
# app.destroy()
