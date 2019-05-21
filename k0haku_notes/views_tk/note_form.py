import tkinter as tk
from tkinter import ttk
from datetime import datetime

from models import TempModel
from .widgets import AutoScrollbar


class AddNotesController:
    def __init__(self, root):
        self.root = root
        self.model = TempModel()

    def subscribe_to_timestamp(self, func):
        """func 
        """
        self.model.timestamp.add_callback(func)

    def load_note(self, id):
        self.model

    def save(self):
        # print(self.model.timestamp.get())
        # print(self.note_form.time_var.get())
        # print(self.model.selected_type.get())
        print(self.model)

    def set_timestamp(self, datetime_string):
        try:
            time = self.model.convert_to_timestamp(datetime_string)
            self.model.timestamp.set(time)
            return True
        except:
            return False

class AddNotesView(tk.Frame):
    def __init__(self, parent, root_controller, id=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = AddNotesController(root_controller)
        if id:
            self.controller.load_note(id)
        self.note_txt = ''
        self.initUI()
        self.controller.set_timestamp(datetime.today())

    def initUI(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollbar = AutoScrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas = tk.Canvas(self, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-1*int(event.delta/120), 'units'))

        self.scrollbar.config(command=self.canvas.yview)

        self.main_frame = tk.Frame(self.canvas)
        self.main_frame.pack(side='top', fill='both', expand=True)

        # TODO: create specialized classes for time field, type dropdown, tag dropdown etc.
        # TIME
        self.time_lbl = ttk.Label(self.main_frame, text='Time:')
        self.time_lbl.pack(side='top', fill='both', expand=True)
        self.time_var = tk.StringVar(self.main_frame)
        self.time_var.trace_add('write', lambda *args: self.on_time_var_change())
        self.controller.subscribe_to_timestamp(lambda timestamp: self.time_var.set(datetime.fromtimestamp(timestamp)))
        self.time_entry = tk.Entry(self.main_frame, textvariable=self.time_var)  # needs to be tk since ttk doesn't have bg colors...
        self.time_entry.pack(side='top', fill='both', expand=True)

        # TODO: hook up the below stuff too like above
        # TYPE
        self.type_lbl = ttk.Label(self.main_frame, text='Type:')
        self.type_lbl.pack(side='top', fill='both', expand=True)
        self.type_var = tk.StringVar(self.main_frame)
        self.type_combobox = ttk.Combobox(self.main_frame, textvariable=self.type_var)
        self.type_combobox.pack(side='top', fill='both', expand=True)

        # TAG
        self.tags_lbl = ttk.Label(self.main_frame, text='Tags:')
        self.tags_lbl.pack(side='top', fill='both', expand=True)
        self.tags_var = tk.StringVar(self.main_frame)
        self.tags_entry = ttk.Entry(self.main_frame, textvariable=self.tags_var)
        self.tags_entry.pack(side='top', fill='both', expand=True)

        # CONTENT
        self.content_lbl = ttk.Label(self.main_frame, text='Content:')
        self.content_lbl.pack(side='top', fill='both', expand=True)

        self.content_var = tk.StringVar(self.main_frame)
        self.content_text = tk.Entry(self.main_frame, textvariable=self.content_var)
        self.content_text.pack(side='top', fill='both', expand=True)

        # COMMENTS
        self.comment_lbl = ttk.Label(self.main_frame, text='Comment:')
        self.comment_lbl.pack(side='top', fill='both', expand=True)

        # TODO: Scrollbar here in case of lots of text?
        self.comment_var = tk.StringVar(self.main_frame)
        self.comment_text = tk.Text(self.main_frame, height=8)
        self.comment_text.bind('<KeyRelease>', lambda e: self.comment_var.set(e.widget.get('1.0', 'end-1c')))
        self.comment_text.insert('1.0', self.note_txt)
        self.comment_text.pack(side='top', fill='both', expand=True)

        # BUTTONS
        self.buttons_down = tk.Frame(self)
        self.buttons_down.grid(row=1, column=0, columnspan=2, sticky='nsew')
        # self.grid_rowconfigure(1, minsize=50, weight=1)
        # self.buttons_down.pack(side='top', fill='both', expand=True)
        self.buttons_down.grid_rowconfigure(0, weight=1, minsize=50)
        self.buttons_down.grid_columnconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(1, weight=1)
        self.buttons_down.grid_columnconfigure(2, weight=1)

        self.savebtn = ttk.Button(self.buttons_down, text='Save')
        self.savebtn.grid(row=0, column=0, columnspan=3, sticky='nswe')
        self.savebtn.config(command=self.controller.save)

        # self.closebtn = ttk.Button(self.buttons_down, text='Close')
        # self.closebtn.grid(row=0, column=2, sticky='nswe')
        # self.closebtn.config(command=self.destroy)

        main_frame_id = self.canvas.create_window(0, 0, anchor='nw', window=self.main_frame)
        self.main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        def on_canvas_configure(event):
            width = event.width
            self.canvas.itemconfigure(main_frame_id, width=width)
        self.canvas.bind('<Configure>', on_canvas_configure)

    def on_time_var_change(self):
        is_success = self.controller.set_timestamp(self.time_var.get())
        if is_success:
            self.time_entry.config(bg='white')
        else:
            self.time_entry.config(bg='red')

    def set_time_bg(self, color):
        self.time_entry.config(bg=color)

    def add_time_callback(self, func):
        self.time_var.trace_add('write', lambda *args: func(self.time_var.get()))

    def set_time(self, time_str):
        self.time_var.set(time_str)

    def add_save_command(self, command):
        self.savebtn.config(command=command)

    def set_types_list(self, types):
        self.type_combobox['values'] = types

    def add_callback_type_create(self, func):
        pass
        # TODO: maybe don't create, only when saving
        # self.type_combobox.bind('<FocusOut>', lambda e: func(self.type_combobox.get()))
        # self.type_combobox.bind('<Return>', lambda e: func(self.type_combobox.get()))
    
    def add_callback_type_select(self, func):
        self.type_combobox.bind('<FocusOut>', lambda e: func(self.type_combobox.get()))
        self.type_combobox.bind('<<ComboboxSelected>>', lambda e: func(self.type_combobox.get()))
    
    def add_callback_tags_select(self, func):
        self.tags_entry.bind('<FocusOut>', lambda e: func(self.tags_entry.get()))
        self.tags_entry.bind('<Return>', lambda e: func(self.tags_entry.get()))

    def add_content_callback(self, func):
        self.content_var.trace_add('write', lambda *args: func(self.content_var.get()))

    def add_comment_callback(self, func):
        self.comment_var.trace_add('write', lambda *args: func(self.comment_var.get()))
