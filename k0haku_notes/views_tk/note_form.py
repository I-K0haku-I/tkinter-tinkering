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
    
    def subscribe_to_selected_type(self, func):
        self.model.selected_type.add_callback(func)
    
    def subscribe_to_type_list(self, func):
        self.model.types_list.add_callback(func)

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

    def set_selected_type(self, type_string):
        self.model.selected_type.set(type_string)
        # TODO: could send back whether type already exists or not
    
    def init_values(self):
        self.set_timestamp(datetime.today())
        self.model.types_list.set(['test','test2'])

class AddNotesView(tk.Frame):
    def __init__(self, parent, root_controller, id=None):
        super().__init__(parent)
        self.parent = parent
        self.controller = AddNotesController(root_controller)
        if id:
            self.controller.load_note(id)
        self.note_txt = ''
        self.init_ui()
        self.controller.init_values()

    def init_ui(self):
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
        self.controller.subscribe_to_timestamp(
            # TODO: maybe create a sub ufnction that delivers the converted daytime isntead of defining it here
            # basically, just make it so you can give in "lambda time: self.time_var.set(time)"
            lambda timestamp: self.time_var.set(str(datetime.fromtimestamp(timestamp))[:-3])
        )
        self.time_entry = tk.Entry(self.main_frame, textvariable=self.time_var)  # needs to be tk since ttk doesn't have bg colors...
        self.time_entry.pack(side='top', fill='both', expand=True)

        # TYPE
        self.type_lbl = ttk.Label(self.main_frame, text='Type:')
        self.type_lbl.pack(side='top', fill='both', expand=True)
        self.type_var = tk.StringVar(self.main_frame)
        self.type_var.trace_add('write', lambda *args: self.on_type_var_change())
        self.controller.subscribe_to_selected_type(lambda new_type: self.type_var.set(new_type))
        self.type_combobox = ttk.Combobox(self.main_frame, textvariable=self.type_var)
        def set_values(values):  # can't do assignmnents in lambadas so have to do this...
            self.type_combobox['values'] = values
        self.controller.subscribe_to_type_list(set_values)
        self.type_combobox.pack(side='top', fill='both', expand=True)

        # TODO: hook up the below stuff too like above
        # TAG
        self.tags_lbl = ttk.Label(self.main_frame, text='Tags:')
        self.tags_lbl.pack(side='top', fill='both', expand=True)
        self.tags_var = tk.StringVar(self.main_frame)
        self.tags_entry = ttk.Entry(self.main_frame, textvariable=self.tags_var)
        self.tags_entry.pack(side='top', fill='both', expand=True)

        # CONTENT
        # TODO: think about putting this at the top or highlighting it or make it easier to click into or something
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
        self.comment_text = tk.Text(self.main_frame, height=20)
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

    def on_type_var_change(self):
        self.controller.set_selected_type(self.type_var.get())

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
