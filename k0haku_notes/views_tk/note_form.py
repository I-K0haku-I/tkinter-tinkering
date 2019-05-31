import tkinter as tk
from tkinter import ttk
from datetime import datetime

from models import NoteModel
from .widgets import AutoScrollbar, ScrollableFrame, TimeField, ComboboxField, EntryField, TextField


class AddNotesAdapter:
    def __init__(self, id=None):
        self.id = id
        self.model = NoteModel()
        self.on_timestamp_validate = lambda bool: None

    def init_values(self):
        if self.id:
            self.model.load(self.id)
        pass
        # self.set_timestamp(datetime.today())
        # self.model.types_list.set(['test', 'test2'])

    def save_note(self):
        # print(self.model.timestamp.get())
        # print(self.note_form.time_var.get())
        # print(self.model.selected_type.get())
        print(self.model)
        self.model.store(self.id)

    def subscribe_to_timestamp(self, func):
        def func_as_str(timestamp):
            func(self.model.convert_to_datetime_str(timestamp))
        self.model.timestamp.add_callback(func_as_str)

    def subscribe_to_selected_type(self, func):
        self.model.selected_type.add_callback(func)

    def subscribe_to_type_list(self, func):
        self.model.types_list.add_callback(func)

    def subscribe_to_tags(self, func):
        def func_as_str(tags_list):
            func(','.join(tags_list))
        self.model.selected_tags_list.add_callback(func_as_str)

    def subscribe_to_content(self, func):
        self.model.content.add_callback(func)

    def subscribe_to_comment(self, func):
        self.model.comment.add_callback(func)

    def set_timestamp(self, datetime_string):
        try:
            time = self.model.convert_to_timestamp(datetime_string)
            self.model.timestamp.set(time)
            self.on_timestamp_validate(True)
        except:
            self.on_timestamp_validate(False)

    def set_selected_type(self, type_string):
        self.model.selected_type.set(type_string)
        # TODO: could send back whether type already exists or not and then display it

    def set_tags(self, tags_str):
        new_tags_list = [tag.strip() for tag in tags_str.split(',')]
        self.model.selected_tags_list.set(new_tags_list)

    def set_content(self, content_str):
        self.model.content.set(content_str)

    def set_comment(self, comment_str):
        self.model.comment.set(comment_str)


class AddNotesView(tk.Frame):
    def __init__(self, parent, id=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = AddNotesAdapter(id)
        self.init_ui()
        self.controller.init_values()
        self.content_field.entry.focus()

    def init_ui(self):
        self.scrollbar = AutoScrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.main_frame = ScrollableFrame(self, self.scrollbar)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content_field = EntryField(self.main_frame, label_text='Content:')
        self.content_field.pack(side='top', fill='both', expand=True)
        self.content_field.entry.bind('<Return>', lambda event: self.save())
        self.content_field.subscribe_to_var(self.controller.set_content)
        self.controller.subscribe_to_content(self.content_field.set_var)

        self.time_field = EntryField(self.main_frame, label_text='Time:')
        self.time_field.pack(side='top', fill='both', expand=True)
        self.time_field.subscribe_to_var(self.controller.set_timestamp)
        self.controller.subscribe_to_timestamp(self.time_field.set_var)
        self.controller.on_timestamp_validate = self.set_time_color

        self.type_field = ComboboxField(self.main_frame, label_text='Type:')
        self.type_field.pack(side='top', fill='both', expand=True)
        self.type_field.subscribe_to_var(self.controller.set_selected_type)
        self.controller.subscribe_to_selected_type(self.type_field.set_var)
        self.controller.subscribe_to_type_list(self.type_field.set_dropdown)

        self.tags_field = EntryField(self.main_frame, label_text='Tags:')
        self.tags_field.pack(side='top', fill='both', expand=True)
        self.tags_field.subscribe_to_var(self.controller.set_tags)
        self.controller.subscribe_to_tags(self.tags_field.set_var)

        self.comment_field = TextField(self.main_frame, label_text='Comment:')
        self.comment_field.pack(side='top', fill='both', expand=True)
        self.comment_field.subscribe_to_var(self.controller.set_comment)
        self.controller.subscribe_to_comment(self.comment_field.set_var)

        self.main_frame.init_scrollbar()

        # # BUTTONS
        # self.buttons_down = tk.Frame(self)
        # self.buttons_down.grid(row=1, column=0, columnspan=2, sticky='nsew')
        # # self.grid_rowconfigure(1, minsize=50, weight=1)
        # # self.buttons_down.pack(side='top', fill='both', expand=True)
        # self.buttons_down.grid_rowconfigure(0, weight=1, minsize=50)
        # self.buttons_down.grid_columnconfigure(0, weight=1)
        # self.buttons_down.grid_columnconfigure(1, weight=1)
        # self.buttons_down.grid_columnconfigure(2, weight=1)

        self.savebtn = ttk.Button(self, text='Save')
        self.savebtn.grid(row=1, column=0, columnspan=2, sticky='nswe')
        self.grid_rowconfigure(1, minsize=50)
        self.savebtn.config(command=self.save)

        # self.closebtn = ttk.Button(self.buttons_down, text='Close')
        # self.closebtn.grid(row=0, column=2, sticky='nswe')
        # self.closebtn.config(command=self.destroy)

    def set_time_color(self, is_valid):
        if is_valid:
            self.time_field.entry.config(bg='white')
        else:
            self.time_field.entry.config(bg='red')
    
    def save(self):
        self.controller.save_note()
        self.parent.destroy()