import tkinter as tk
import os
from pathlib import Path
from datetime import datetime
from tkinter import ttk
from tkinter import N, E, S, W

from .add_notes import AddNotesWindow
from .start_page import StartPage


class NoteOverview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrlr = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, pad=7)

        label = ttk.Label(self, text='First Page')
        label.grid(row=0, column=0)
    
        self.listbox = tk.Listbox(self)
        self.listbox.insert(tk.END, '...')
        notes = Path(controller.notes_path.get())
        if not notes.exists():
            notes.mkdir()
        files = os.listdir(controller.notes_path.get()) # TODO: load from current working path
        # TODO: need to separate dirs and files, dirs should end with a slash and be on top
        for file in files:
            self.listbox.insert(tk.END, file)

        self.listbox.bind('<Double-1>', self.on2ClickItem)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky=N+E+S+W)

        self.buttons_down = tk.Frame(self)
        self.buttons_down.grid(row=2, column=0, sticky=N+E+S+W)
        self.add_today_btn = ttk.Button(
            self.buttons_down, text='Add Today', command=self.add_current_date)
        self.add_today_btn.pack(side='left', fill='both', expand=True)

        # TODO: disable if file already exists
        # self.add_today_btn['default'] = tk.DISABLED

        self.create_btn = ttk.Button(
            self.buttons_down, text='New File...', command=self.create_new_file)
        self.create_btn.pack(side='left', fill='both', expand=True)

        self.back_btn = ttk.Button(
            self.buttons_down, text='Back', command=lambda: controller.show_frame(StartPage))
        self.back_btn.pack(side='left', fill='both', expand=True)

    def add_current_date(self):
        time = datetime.now()
        year, month, day = (str(time.year), str(time.month), str(time.day))
        root = Path(self.ctrlr.notes_path.get())
        year_path = root / year
        if not os.path.isdir(year_path):
            os.mkdir(year_path)
        month_path = year_path / month
        if not os.path.isdir(month_path):
            os.mkdir(month_path)
        day_path = month_path / (day + '.note')
        open(day_path, 'a').close()
        self.ctrlr.show_frame(NoteOverview)

        # NOTE: maybe I could use a proper db for this

    def create_new_file(self):
        print('hi')

    def on2ClickItem(self, event):
        name = self.listbox.selection_get()
        print((Path(self.ctrlr.notes_path.get()) / Path(name)))
        if name == '...':
            print('TODO: implement return to upper level directory')
            # but prevent returning if in root
            return
        # !!!!!!TODO: check if dir and load it in this frame instead
        if Path(name).is_dir():
            print('yes') 
        # TODO: if selected node is dir
        # then add node to list of nodes and show this frame again

        # self.ctrlr.selected_file.set(name)
        # self.ctrlr.show_frame(AddNotesWindow)