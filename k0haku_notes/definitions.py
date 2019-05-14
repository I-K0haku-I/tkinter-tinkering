import tkinter as tk
from tkinter import ttk


def create_popup(title='Popup', msg='', buttons=('OK',)):
    popup = tk.Toplevel()
    popup.title(title)
    label = ttk.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)
    for b in buttons:
        B1 = ttk.Button(popup, text=b, command=popup.destroy)
        B1.pack()


# This feels like a bad idea, I think I should just write out the menu in the menu
SUBMENU_COMMANDS = {
    'Add file...': lambda: create_popup(),
    'Settings': lambda: print('lul'),
    'Exit': quit
}
