import tkinter as tk
import os
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
        try:
            files = os.listdir(controller.notes_path.get())
        except FileNotFoundError:
            os.mkdir(os.getcwd()+controller.notes_path.get())
            files = os.listdir(controller.notes_path.get())

        self.listbox = tk.Listbox(self)
        self.listbox.insert(tk.END, '...')
        for file in files:
            self.listbox.insert(tk.END, file)

        self.listbox.bind('<Double-1>', self.on2ClickItem)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky=N+E+S+W)

        self.buttons_down = tk.Frame(self)
        self.buttons_down.grid(row=2, column=0, sticky=N+E+S+W)
        self.create_btn = ttk.Button(
            self.buttons_down, text='New File...', command=self.create_new_file)
        self.create_btn.pack(side='left', fill='both', expand=True)
        self.create_btn2 = ttk.Button(
            self.buttons_down, text='Back', command=lambda: controller.show_frame(StartPage))
        self.create_btn2.pack()
        self.create_btn2.pack(side='left', fill='both', expand=True)

    def create_new_file(self):
        print('hi')

    def on2ClickItem(self, event):
        name = self.listbox.selection_get()
        if name == '...':
            print('TODO: implement return to upper level directory')
            return
        self.ctrlr.selected_file.set(name)
        self.ctrlr.show_frame(AddNotesWindow)
