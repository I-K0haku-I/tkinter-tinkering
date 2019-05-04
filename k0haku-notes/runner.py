import tkinter as tk

from utils.helpers import FrameHolder

from notes import create_popup
from frames import StartPage, AddNotesWindow
from frames.start_page import StartPageController
from frames.add_notes import AddNotesWindowController


class NotesAppController:
    def __init__(self, *args, **kwargs):
        self.view = NotesAppView(self)

        self.view.mainloop()
        self.view.destroy()


class NotesAppView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Notes')
        self.geometry('640x500')
        self.menubar = NotesAppMenu(self)
        self.config(menu=self.menubar)

        self.body = FrameHolder(self, controller)
        self.body.add(StartPage)
        self.body.add(AddNotesWindow)
        self.body.show(StartPage)


class NotesAppMenu(tk.Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.submenu = tk.Menu(self, tearoff=0)
        self.submenu.add_command(label='Add file...', command=lambda: create_popup())
        self.submenu.add_command(label='Settings', command=lambda: print('lul'))
        self.submenu.add_separator()
        self.submenu.add_command(label='Exit', command=quit)

        self.subsubmenu = tk.Menu(self.submenu, tearoff=0)
        self.subsubmenu.add_command(label='Exit', command=quit)
        self.subsubmenu.add_checkbutton(label='check')
        self.subsubmenu.add_separator()
        self.subsubmenu.add_radiobutton(label='radio')
        self.subsubmenu.add_radiobutton(label='radio2')

        self.submenu.add_cascade(label='TEST', menu=self.subsubmenu)

        self.add_cascade(label='Stuff...', menu=self.submenu)
        self.add_cascade(label='Stuff2...', menu=self.submenu)
        self.add_cascade(label='Stuff3...', menu=self.subsubmenu)


if __name__ == "__main__":
    app = NotesAppController()
