import tkinter as tk
import os
from tkinter import ttk

from .add_notes import AddNotesWindow

class NoteOverview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrlr = controller
        label = ttk.Label(self, text='First Page')
        label.pack(pady=10, padx=10)
        
        files = os.listdir(controller.notes_path.get())

        self.listbox = tk.Listbox(self)
        self.listbox.insert(tk.END, '...')
        for file in files:
            self.listbox.insert(tk.END, file)

        self.listbox.bind('<Double-1>', self.on2ClickItem)
        self.listbox.pack(pady=15)

    def on2ClickItem(self, event):
        name = self.listbox.selection_get()
        self.ctrlr.selected_file.set(name)
        self.ctrlr.show_frame(AddNotesWindow)