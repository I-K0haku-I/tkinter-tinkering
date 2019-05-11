import tkinter as tk

from utils.helpers import FrameHolder

from notes import create_popup
from frames import StartPage, AddNotesWindow
from frames.start_page import StartPageController
from frames.add_notes import AddNotesWindowController

class TempModel:
    def __init__(self, parent):
        self.time = tk.StringVar(parent)


# TODO: add logic for saving stuff to files
def save_to_file(file, text):
    print('TODO: implement saving text to file')


class NotesAppController:
    def __init__(self, *args, **kwargs):
        self.controllers = {}
        self.file_path = 'test'
        self.save_callback = save_to_file

        self.view = NotesAppView(self)
        self.model = TempModel(self.view)

        self.add_notes_view = self.get_instance_in_frame(AddNotesWindow)
        self.add_notes_view.savebtn.config(command=self.save)
        self.add_notes_view.closebtn.config(command=lambda: self.show(StartPage))
        self.add_notes_view.time_entry.config(textvariable=self.model.time)

        self.start_page_view = self.get_instance_in_frame(StartPage)
        self.start_page_view.button.config(command=lambda: self.show(AddNotesWindow))

        self.show(StartPage)

        self.view.mainloop()
        self.view.destroy()

    def save(self):
        if self.save_callback:
            text = self.add_notes_view.content_text.get('1.0', 'end-1c')
            self.save_callback(self.file_path, text)

    def get_instance_in_frame(self, View):
        return self.view.frame.views.get(View)

    def show(self, View):  # not sure if this should go in FrameHolder or not
        self.get_instance_in_frame(View).tkraise()

        # frame = getattr(self.controllers.get(View), 'view', None)
        # if frame is not None:
        #     frame.destroy()
        # frame = View(self, self.main_controller)
        # frame.grid(row=0, column=0, sticky='nsew')
        # self.frames[View] = frame


class NotesAppView(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Notes')
        self.geometry('640x500')
        self.menubar = NotesAppMenu(self)
        self.config(menu=self.menubar)

        self.frame = FrameHolder(self)
        self.frame.add(StartPage)
        self.frame.add(AddNotesWindow)


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
