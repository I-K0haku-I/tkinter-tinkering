import tkinter as tk

from frames.add_notes import AddNotesWindow, AddNotesWindowController
from frames.start_page import StartPage, StartPageController


class FrameHolder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(side='top', fill='both', expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.views = {}
        self.selected_frame = None

    def add(self, View):
        view = View(self)
        view.grid(row=0, column=0, sticky='nsew')
        self.views[View] = view
