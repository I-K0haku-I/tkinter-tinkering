from tkinter import ttk
import tkinter as tk

from frames.add_notes import AddNotesWindow


class StartPageController:
    def __init__(self, view, controller):
        self.parent_controller = controller
        self.view = view
        self.view.button.config(command=lambda: self.open_add_notes())

    def open_add_notes(self):
        self.parent_controller.show(AddNotesWindow)


class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text='Hello World')
        label.pack(pady=10, padx=10)

        self.button = ttk.Button(self, text='ACTUALLY Start App')
        self.button.pack()
