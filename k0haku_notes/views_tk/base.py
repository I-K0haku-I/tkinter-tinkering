import tkinter as tk
from tkinter import ttk
from .widgets import FrameHolder

from .note_form import AddNotesWindow
from .start_page import StartPage
from definitions import SUBMENU_COMMANDS


class NotesAppView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Notes')
        self.geometry('640x500')
        
        self.menubar = NotesAppMenu(self)
        menu = self.menubar.subsubmenu
        menu.entryconfigure(menu.index('Exit'), command=lambda: self.change_interior_to(StartPage))
        menu = self.menubar.submenu
        for name, command in SUBMENU_COMMANDS.items():
            menu.entryconfigure(menu.index(name), command=command)
        self.config(menu=self.menubar)

    
        self.frame = FrameHolder(self)
        start_page = self.frame.add(StartPage)
        start_page.button.config(command=lambda: self.change_interior_to(AddNotesWindow))
        add_notes = self.frame.add(AddNotesWindow)
        add_notes.closebtn.config(command=lambda: self.change_interior_to(StartPage))
    
    def change_interior_to(self, View):
        self.frame.views.get(View).tkraise()
    
    def get_interior(self, View):
        return self.frame.views.get(View)
        

class NotesAppMenu(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.submenu = tk.Menu(self, tearoff=0)
        for name in SUBMENU_COMMANDS.keys():
            self.submenu.add_command(label=name)
        self.submenu.insert_separator(2)

        self.subsubmenu = tk.Menu(self.submenu, tearoff=0)
        
        self.subsubmenu.add_command(label='Exit')
        self.subsubmenu.add_checkbutton(label='check')
        self.subsubmenu.add_separator()
        self.subsubmenu.add_radiobutton(label='radio')
        self.subsubmenu.add_radiobutton(label='radio2')

        self.submenu.add_cascade(label='TEST', menu=self.subsubmenu)

        self.add_cascade(label='Stuff...', menu=self.submenu)
        self.add_cascade(label='Stuff2...', menu=self.submenu)
        self.add_cascade(label='Stuff3...', menu=self.subsubmenu)
