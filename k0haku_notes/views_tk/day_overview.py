import tkinter as tk
from tkinter import ttk


class DayOverviewController:
    def __init__(self, root):
        self.root = root

    def get_selected_note_id(self):
        data = self.root
        return data

class DayOverview(tk.Frame):
    def __init__(self, parent, root_controller):
        super().__init__(parent)
        self.grid_columnconfigure(1, weight=1, minsize=70)
        self.grid_columnconfigure(0, weight=1, minsize=300)

        self.controller = DayOverviewController(root_controller)

        tree = BetterTreeview(self)
        tree.set_headers((('time', 50), ('note', 200), ('type', 50)))
        tree.grid(row=0, column=0, sticky='nsew')

        menu = tk.Frame(self, width=100)
        menu.grid(row=0, column=1, sticky='nsew')
        add_btn = tk.Button(menu, text='Add')
        add_btn.config(command=self.create_add_note)
        add_btn.pack(side='top', fill='both')
        edit_btn = tk.Button(menu, text='Edit')
        edit_btn.pack(side='top', fill='both')
        
        self.treeview = tree
        self.add_btn = add_btn
        self.edit_btn = edit_btn
    
    def create_add_note(self):
        id = self.controller.get_selected_note_id()
        new_window = tk.Toplevel(self)
        from .note_form import AddNotesView
        add_note = AddNotesView(new_window, self.controller.root, id=id)
        add_note.pack(side='top', fill='both', expand=True)


class BetterTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['show'] = 'headings'
    
    def set_headers(self, headers_tuple):
        header_names = tuple(h[0] for h in headers_tuple)
        self['columns'] = header_names
        for header, width in headers_tuple:
            self.heading(header, text=header, anchor='w')
            self.column(header, width=width)
    
    def append(self, values):
        self.insert('', 'end', value=values)