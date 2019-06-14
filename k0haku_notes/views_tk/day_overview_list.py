import tkinter as tk
from tkinter import ttk

from logic.day_overview import DayOverviewController


class DayOverview(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(1, weight=1, minsize=70)
        self.grid_columnconfigure(0, weight=1, minsize=300)

        self.controller = DayOverviewController()

        tree = BetterTreeview(self)
        tree.set_headers((('time', 120), ('note', 250), ('type', 80), ('tags', 150)))
        tree.grid(row=0, column=0, sticky='nsew')
        tree.on_append_func = self.controller.note_list.append_without_event
        self.controller.note_list.on_append_func = tree.append_without_event

        # Frame of buttons
        menu = tk.Frame(self, width=100)
        menu.grid(row=0, column=1, sticky='nsew')
        add_btn = tk.Button(menu, text='Add')
        add_btn.config(command=self.create_add_note)
        add_btn.pack(side='top', fill='both')
        edit_btn = tk.Button(menu, text='Edit')
        edit_btn.config(command=self.create_edit_note)
        edit_btn.pack(side='top', fill='both')
        test_add_btn = tk.Button(menu, text='Add Dummy')
        test_add_btn.config(command=self.add_dummy)
        test_add_btn.pack(side='top', fill='both')

        self.treeview = tree
        self.add_btn = add_btn
        self.edit_btn = edit_btn

        self.controller.init_values()
    
    def add_dummy(self):
        self.treeview.append(('test', 'te', '3', '523'))

    def create_add_note(self):
        new_window = tk.Toplevel(self)
        from .note_form import AddNotesView
        add_note = AddNotesView(new_window)
        add_note.pack(side='top', fill='both', expand=True)
        
    def create_edit_note(self):
        id = self.controller.get_selected_note_id()
        new_window = tk.Toplevel(self)
        from .note_form import AddNotesView
        add_note = AddNotesView(new_window, id=id)
        add_note.pack(side='top', fill='both', expand=True)
        

class BetterTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['show'] = 'headings'
        self['selectmode'] = 'browse'
        self.on_append_func = lambda values: None

    def set_headers(self, headers_tuple):
        header_names = tuple(h[0] for h in headers_tuple)
        self['columns'] = header_names
        for header, width in headers_tuple:
            self.heading(header, text=header, anchor='w')
            self.column(header, width=width)

    def append_without_event(self, values):
        # attach to root, append to end, values is tuple of values to add
        self.insert('', 'end', value=values)    

    def append(self, values):  # TODO: add event for appending here
        self.append_without_event(values)
        self.on_append_func(values)
