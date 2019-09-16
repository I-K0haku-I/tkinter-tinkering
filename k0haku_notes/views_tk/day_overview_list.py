import datetime

import tkinter as tk
from tkinter import ttk

from logic.day_overview import DayOverviewController


class DayOverview(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=0, minsize=150)
        self.grid_rowconfigure(0, weight=0, minsize=70)
        self.grid_rowconfigure(1, weight=1, minsize=350)

        self.controller = DayOverviewController()

        top_box = tk.Frame(self, background='red')
        top_box.grid(row=0, column=0, sticky='nsew')

        navigation = tk.Frame(top_box, background='blue')
        navigation.pack(fill='both', expand=True)
        # navigation.place(relx=0.5, rely=0.5, anchor='center')

        left_btn = tk.Button(navigation, text='<-')
        left_btn.pack(side='left', expand=True, fill='both')
        left_btn.config(command=self.controller.prev_day, font=("Courier", 15))

        date_var = tk.StringVar()
        date_var.set('TESTSS')
        date_var.trace_add('write', lambda *args: self.controller.date.set_string(date_var.get()))
        self.controller.date.on_change(lambda data: date_var.set(data))

        date_lbl = tk.Label(navigation, textvariable=date_var, width=20)
        date_lbl.pack(side='left', expand=True, fill='both')
        date_lbl.config(font=('Courier', 15))

        right_btn = tk.Button(navigation, text='->')
        right_btn.pack(side='left', expand=True, fill='both')
        right_btn.config(command=self.controller.next_day, font=("Courier", 15))

        tree = BetterTreeview(self)
        tree.set_headers((('time', 120), ('note', 350), ('type', 80), ('tags', 150)))
        tree.grid(row=1, column=0, sticky='nsew')
        tree.bind('<Double-1>', lambda event: self.create_edit_note())
        tree.on_add_item_func = self.controller.note_list.add_item_without_event
        self.controller.note_list.on_add_item_func = tree.add_item_without_event
        self.controller.note_list.on_set_by_func = tree.set_by_index
        self.controller.note_list.on_move_item_func = tree.move_item

        # Frame of buttons
        menu = tk.Frame(self, width=100)
        menu.grid(row=1, column=1, sticky='nsew')

        button_kwargs = dict(ipady=31, ipadx=50)

        add_btn = tk.Button(menu, text='Add')
        add_btn.config(command=self.create_add_note)
        add_btn.pack(side='top', fill='both', **button_kwargs)

        edit_btn = tk.Button(menu, text='Edit')
        edit_btn.config(command=self.create_edit_note)
        edit_btn.pack(side='top', fill='both', **button_kwargs)

        delete_btn = tk.Button(menu, text='Delete')
        delete_btn.config(command=self.delete_note)
        delete_btn.pack(side='top', fill='both', **button_kwargs)

        refresh_btn = tk.Button(menu, text='Refresh')
        refresh_btn.config(command=self.controller.refresh)
        refresh_btn.pack(side='top', fill='both', **button_kwargs)

        self.treeview = tree
        self.add_btn = add_btn
        self.edit_btn = edit_btn

        self.controller.clear_list_func = self.clear_list
        # self.controller.init_values(async_mode=True)

    def clear_list(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def create_note_popup(self, id=None, on_store_data=lambda note: None, time=None):
        new_window = tk.Toplevel(self)
        from .note_form import AddNotesView
        add_note = AddNotesView(new_window, id=id, time=time)
        add_note.pack(side='top', fill='both', expand=True)
        add_note.on_store_data = on_store_data

    def create_add_note(self):
        if self.controller.date.get(as_string=False) == datetime.date.today():
            time_to_use = datetime.datetime.now()
        else:
            time_to_use = datetime.datetime.combine(self.controller.date.get(as_string=False), datetime.datetime.min.time())
        self.create_note_popup(on_store_data=self.controller.add_note, time=time_to_use)

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


class Navigation():
    pass


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
