import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk

from models import TempModel
from views_tk.base import NotesAppView
from views_tk.note_form import AddNotesWindow
from views_tk.start_page import StartPage
from definitions import SUBMENU_COMMANDS

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_NOTES_PATH = ROOT_DIR + '\\data\\notes\\'


# TODO: add logic for saving stuff to files
def save_to_file(file, text):
    print('TODO: implement saving text to file')


class NotesAppController:
    def __init__(self, *args, **kwargs):
        self.controllers = {}
        self.file_path = 'test'
        self.save_callback = save_to_file

        self.view = NotesAppView(self)
        self.add_notes_view = self.view.get_interior(AddNotesWindow)
        self.start_page_view = self.view.get_interior(StartPage)

        self.model = TempModel(self)

        self.add_notes_view.savebtn.config(command=self.save)

        self.add_notes_view.AddTimeCallback(lambda datetime_str: self.set_timestamp(datetime_str))
        self.model.timestamp.AddCallback(lambda timestamp: self.add_notes_view.time_var.set(datetime.fromtimestamp(timestamp)))
        time = datetime.today()
        self.set_timestamp(time)

        # start view loop
        self.view.change_interior_to(StartPage)
        self.view.mainloop()
    
    def set_timestamp(self, datetime_string):
        try:
            time = datetime.fromisoformat(str(datetime_string)).replace(microsecond=0).timestamp()
            self.model.timestamp.set(time)
            self.add_notes_view.set_time_bg('white')
        except:
            self.add_notes_view.set_time_bg('red')

    def save(self):
        print(self.model.timestamp.get())
        print(self.add_notes_view.time_var.get())
        if self.save_callback:
            text = self.add_notes_view.content_text.get('1.0', 'end-1c')
            self.save_callback(self.file_path, text)

    def show(self, View):  # not sure if this should go in FrameHolder or not
        self.view.change_interior_to(View)

        # frame = getattr(self.controllers.get(View), 'view', None)
        # if frame is not None:
        #     frame.destroy()
        # frame = View(self, self.main_controller)
        # frame.grid(row=0, column=0, sticky='nsew')
        # self.frames[View] = frame