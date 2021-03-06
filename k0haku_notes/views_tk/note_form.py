import functools
import asyncio
import tkinter as tk
from tkinter import ttk

from logic.note import AddNotesAdapter
from .widgets import AutoScrollbar, ScrollableFrame, TimeField, ComboboxField, EntryField, TextField, DurationField


class AddNotesView(tk.Frame):
    def __init__(self, parent, id=None, time=None):
        super().__init__(parent)
        self.parent = parent

        self.on_store_data = lambda note: None
        # self.save_callbacks = []
        # self.save_callbacks.append(self.store_data)

        self.controller = AddNotesAdapter(id)
        self.init_ui()
        self.controller.init_values(time)

        self.content_field.entry.focus()

    def init_ui(self):
        self.scrollbar = AutoScrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.main_frame = ScrollableFrame(self, self.scrollbar)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1, minsize=500)
        self.grid_rowconfigure(1, weight=0, minsize=100)
        self.grid_columnconfigure(0, weight=1)

        self.content_field = EntryField(self.main_frame, label_text='Content:')
        self.content_field.pack(side='top', fill='both', expand=True)
        self.content_field.entry.bind('<Return>', lambda event: self.save())
        self.content_field.on_write(self.controller.content.set)
        self.controller.content.on_change(self.content_field.set_var)

        self.time_field = EntryField(self.main_frame, label_text='Time:')
        self.time_field.pack(side='top', fill='both', expand=True)
        self.time_field.on_write(lambda val: self.controller.timestamp.set_string(val, self.get_color_func(self.time_field.entry)))
        self.controller.timestamp.on_change(self.time_field.set_var)

        # self.duration_frame = tk.Frame(self.main_frame)
        # self.duration_frame.pack(side='top', fill='both', expand=True)
    
        self.duration_field = DurationField(self.main_frame, label_text='Duration:')
        # self.duration_field.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.duration_field.pack(side='top', fill='both', expand=True)
        self.duration_field.on_write(lambda val: self.controller.duration.set_string(val, self.get_color_func(self.duration_field.entry)))
        self.controller.duration.on_change(self.duration_field.set_var)
        self.duration_field.stop_btn.config(command=self.controller.calc_duration)
        # self.stop_btn = tk.Button(self.duration_frame, text='!')
        # self.stop_btn.pack(side='left', fill='both', expand=True)
        # self.stop_btn.grid(row=0, column=3, sticky='nsew')

        # self.type_field = ComboboxField(self.main_frame, label_text='Type:')
        # self.type_field.pack(side='top', fill='both', expand=True)
        # self.type_field.on_write(self.controller.selected_type.set)
        # self.controller.selected_type.on_change(self.type_field.set_var)
        # self.controller.types_list.on_change(self.type_field.set_dropdown)

        self.tags_field = EntryField(self.main_frame, label_text='Tags:')
        self.tags_field.pack(side='top', fill='both', expand=True)
        self.tags_field.on_write(self.controller.selected_tags_list.set_string)
        self.controller.selected_tags_list.on_change(self.tags_field.set_var)

        self.comment_field = TextField(self.main_frame, label_text='Comment:')
        self.comment_field.pack(side='top', fill='both', expand=True)
        self.comment_field.on_write(self.controller.comment.set)
        self.controller.comment.on_change(self.comment_field.set_var)

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
        # self.savebtn.pack(side='right', fill='both', expand=True)
        # self.grid_rowconfigure(1, minsize=100)
        self.savebtn.config(command=self.save)

        # self.closebtn = ttk.Button(self.buttons_down, text='Close')
        # self.closebtn.grid(row=1, column=1, sticky='nswe')
        # self.closebtn.pack(side='right', fill='both', expand=True)
        # self.closebtn.config(command=self.destroy)
    
    def get_color_func(self, elem):
        return functools.partial(self.set_color, elem)

    def set_color(self, elem, is_valid):
        if is_valid:
            elem.config(bg='white')
        else:
            elem.config(bg='red')

    def save(self):
        # for call in self.save_callbacks:
        #     call()
        self.store_data()
        self.parent.destroy()

    def store_data(self):
        asyncio.create_task(self.store_data_async())

    async def store_data_async(self):
        new_data = await self.controller.store_async()
        self.on_store_data(new_data)
