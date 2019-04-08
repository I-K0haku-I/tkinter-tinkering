from tkinter import ttk 
import tkinter as tk


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text='Hello World')
        label.pack(pady=10, padx=10)

        from app.stuff import ViewRefs
        button = ttk.Button(self, text='ACTUALLY Start App', command=lambda: controller.show_frame(ViewRefs.START))
        button.pack()