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
        tree.set_headers((('time', 120), ('note', 350), ('type', 80), ('tags', 150)))
        tree.grid(row=0, column=0, sticky='nsew')
        tree.bind('<Double-1>', lambda event: self.create_edit_note())
        tree.on_add_item_func = self.controller.note_list.add_item_without_event
        self.controller.note_list.on_add_item_func = tree.add_item_without_event
        self.controller.note_list.on_set_by_func = tree.set_by_index
        self.controller.note_list.on_move_item_func = tree.move_item

        # Frame of buttons
        menu = tk.Frame(self, width=100)
        menu.grid(row=0, column=1, sticky='nsew')

        add_btn = tk.Button(menu, text='Add')
        add_btn.config(command=self.create_add_note)
        add_btn.pack(side='top', fill='both')

        edit_btn = tk.Button(menu, text='Edit')
        edit_btn.config(command=self.create_edit_note)
        edit_btn.pack(side='top', fill='both')

        delete_btn = tk.Button(menu, text='Delete')
        delete_btn.config(command=self.delete_note)
        delete_btn.pack(side='top', fill='both')

        refresh_btn = tk.Button(menu, text='Refresh')
        refresh_btn.config(command=self.refresh_list)
        refresh_btn.pack(side='top', fill='both')

        self.treeview = tree
        self.add_btn = add_btn
        self.edit_btn = edit_btn

        self.controller.init_values()

    def refresh_list(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        self.controller.init_values()

    def create_note_popup(self, id=None, on_store_data=lambda note: None):
        new_window = tk.Toplevel(self)
        from .note_form import AddNotesView
        add_note = AddNotesView(new_window, id=id)
        # add_note.save_callbacks.append(self.refresh_list)
        add_note.pack(side='top', fill='both', expand=True)
        add_note.on_store_data = on_store_data

    def create_add_note(self):
        self.create_note_popup(on_store_data=self.controller.add_note)

    def create_edit_note(self):
        item = self.treeview.focus()
        if item is None:
            return
        index = self.treeview.index(item)
        id = self.controller.get_selected_note_id(index)
        self.create_note_popup(id=id, on_store_data=self.controller.edit_note)

    def delete_note(self):
        item = self.treeview.focus()
        if item is None:
            return
        index = self.treeview.index(item)
        if self.controller.delete(index):
            self.treeview.delete(item)
        # print([self.treeview.item(i, 'values')[4] for i in self.treeview.get_children()], '\n', [n[4] for n in self.controller.note_list.get()])


class BetterTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['show'] = 'headings'
        self['selectmode'] = 'browse'
        self.on_add_item_func = lambda values, index: None

    def set_headers(self, headers_tuple):
        header_names = tuple(h[0] for h in headers_tuple)
        self['columns'] = header_names
        for header, width in headers_tuple:
            self.heading(header, text=header, anchor='w')
            self.column(header, width=width)

    def set_by_index(self, index, value):
        for i, item in enumerate(self.get_children()):
            if i == index:
                self.item(item, values=value)
                return

    def move_item(self, old_index, new_index):
        old_item = self.get_children()[old_index]
        self.move(old_item, '', new_index)

    def add_item_without_event(self, values, index=None):
        # attach to root, append to end, values is tuple of values to add
        # hmmm
        # if index is not None and index < len(self.get_children()):
        #     self.delete(self.get_children()[index])
        self.insert('', 'end' if index is None else index, value=values)

    def add_item(self, values, index=None):  # TODO: add event for appending here
        self.add_item_without_event(values, 'end' if index is None else index)
        self.on_add_item_func(values, index)
