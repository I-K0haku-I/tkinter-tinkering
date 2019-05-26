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
        self.model.timestamp.add_callback(func)
    
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
        # TODO: could send back whether type already exists or not and then display it
    
    def set_tags(self, tags_str):
        new_tags_list = [tag.strip() for tag in tags_str.split(',')]
        self.model.selected_tags_list.set(new_tags_list)

    def set_content(self, content_str):
        self.model.content.set(content_str)

    def set_comment(self, comment_str):
        self.model.comment.set(comment_str)

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

        self.time_lbl, self.time_var, self.time_entry = self.create_time(self.main_frame)
        self.type_lbl, self.type_var, self.type_combobox = self.create_type(self.main_frame)
        # TODO: hook up the below stuff too like above
        self.tags_lbl, self.tags_var, self.tags_entry = self.create_tags(self.main_frame)
        # TODO: think about putting content at the top or highlighting it or make it easier to click into or something
        self.content_lbl, self.content_var, self.content_entry = self.create_content(self.main_frame)
        self.comment_lbl, self.comment_var, self.comment_text = self.create_comment(self.main_frame)

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
    
    def create_time(self, parent):
        label = ttk.Label(parent, text='Time:')
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(parent)
        var.trace_add('write', lambda *args: self.on_time_change())
        self.controller.subscribe_to_timestamp(
            # TODO: maybe create a sub ufnction that delivers the converted daytime isntead of defining it here
            # basically, just make it so you can give in "lambda time: self.time_var.set(time)"
            lambda timestamp: var.set(str(datetime.fromtimestamp(timestamp))[:-3])
        )

        entry = tk.Entry(parent, textvariable=var)  # needs to be tk since ttk doesn't have bg colors...
        entry.pack(side='top', fill='both', expand=True)

        return label, var, entry

    def on_time_change(self):
        is_success = self.controller.set_timestamp(self.time_var.get())
        if is_success:
            self.time_entry.config(bg='white')
        else:
            self.time_entry.config(bg='red')
    
    def create_type(self, parent):
        label = ttk.Label(parent, text='Type:')
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(parent)
        var.trace_add('write', lambda *args: self.on_type_var_change())
        self.controller.subscribe_to_selected_type(lambda new_type: var.set(new_type))

        combobox = ttk.Combobox(parent, textvariable=var)
        def set_values(values):  # can't do assignmnents in lambadas so have to do this...
            combobox['values'] = values
        self.controller.subscribe_to_type_list(set_values)
        combobox.pack(side='top', fill='both', expand=True)

        return label, var, combobox

    def on_type_var_change(self):
        self.controller.set_selected_type(self.type_var.get())
    
    def create_tags(self, parent):
        label = ttk.Label(parent, text='Tags:')
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(parent)
        var.trace_add('write', lambda *args: self.on_tags_var_change())
        self.controller.subscribe_to_tags(lambda new_tags: var.set(new_tags))

        entry = ttk.Entry(parent, textvariable=var)
        entry.pack(side='top', fill='both', expand=True)

        return label, var, entry
    
    def on_tags_var_change(self):
        self.controller.set_tags(self.tags_var.get())
    
    def create_content(self, parent):
        label = ttk.Label(parent, text='Content:')
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(parent)
        var.trace_add('write', lambda *args: self.on_content_var_change())
        self.controller.subscribe_to_content(lambda new_content: var.set(new_content))

        entry = tk.Entry(parent, textvariable=var)
        entry.pack(side='top', fill='both', expand=True)

        return label, var, entry
    
    def on_content_var_change(self):
        self.controller.set_content(self.content_var.get())
    
    def create_comment(self, parent):
        # TODO: Scrollbar here in case of lots of text?
        label = ttk.Label(parent, text='Comment:')
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(parent)
        var.trace_add('write', lambda *args: self.on_comment_var_change())
        self.controller.subscribe_to_comment(lambda new_comment: var.set(new_comment))
    
        text = tk.Text(parent, height=20)
        text.bind('<KeyRelease>', lambda e: var.set(e.widget.get('1.0', 'end-1c')))
        # text.insert('1.0', self.note_txt)
        text.pack(side='top', fill='both', expand=True)

        return label, var, text

    def on_comment_var_change(self):
        self.controller.set_comment(self.comment_var.get())