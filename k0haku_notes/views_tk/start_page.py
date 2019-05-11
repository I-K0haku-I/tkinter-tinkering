import tkinter as tk
from tkinter import ttk


class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text='Hello World')
        label.pack(pady=10, padx=10)

        self.button = ttk.Button(self, text='ACTUALLY Start App')
        self.button.pack()
