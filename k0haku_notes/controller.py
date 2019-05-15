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
    SUBMENU_COMMANDS = SUBMENU_COMMANDS

    def __init__(self, *args, **kwargs):
        self.controllers = {}
        self.file_path = 'test'
        self.save_callback = save_to_file

        self.view = NotesAppView(self)
        self.model = TempModel(self)

        timestamp_var = self.model.timestamp
        types_list = self.model.types_list

        # VIEW: START PAGE
        start_page: StartPage = self.view.get_interior(StartPage)

        # VIEW: ADD NOTES
        # TODO: create a class for note_form that takes the AddNotesWindow instance
        note_form: AddNotesWindow = self.view.get_interior(AddNotesWindow)
        note_form.add_save_command(self.save)
        def update_model(datetime_str):
            return self.set_timestamp(datetime_str)
        def update_view_state(timestamp):
            return note_form.set_time(datetime.fromtimestamp(timestamp))
        note_form.add_time_callback(update_model)
        timestamp_var.add_callback(update_view_state)

        # note_form.add_type_callback(lambda type:)
        def update_view_state(types):
            return note_form.set_types_list(types)
        types_list.add_callback(update_view_state)
        note_form.add_callback_type_create(self.create_type)

        self.start_page = start_page
        self.note_form = note_form
        # START view loop
        self.set_timestamp(datetime.today())
        types_list.set(['test','test2'])
        self.view.change_interior_to(StartPage)
        self.view.mainloop()

    def create_type(self, new_type):
        if new_type in self.model.types_list.get():
            return
        self.model.types_list.set(self.model.types_list.get() + [new_type])
        self.model.selected_type.set(new_type)

    def set_timestamp(self, datetime_string):
        try:
            time = datetime.fromisoformat(str(datetime_string)).replace(microsecond=0).timestamp()
            self.model.timestamp.set(time)
            self.note_form.set_time_bg('white')
        except:
            self.note_form.set_time_bg('red')

    def save(self):
        print(self.model.timestamp.get())
        print(self.note_form.time_var.get())
        print(self.model.selected_type.get())
        if self.save_callback:
            text = self.note_form.content_text.get('1.0', 'end-1c')
            self.save_callback(self.file_path, text)

    def show(self, View):  # not sure if this should go in FrameHolder or not
        self.view.change_interior_to(View)

        # frame = getattr(self.controllers.get(View), 'view', None)
        # if frame is not None:
        #     frame.destroy()
        # frame = View(self, self.main_controller)
        # frame.grid(row=0, column=0, sticky='nsew')
        # self.frames[View] = frame