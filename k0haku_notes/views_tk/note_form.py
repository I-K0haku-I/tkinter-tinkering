import tkinter as tk
from tkinter import ttk

from .widgets import AutoScrollbar


class AddNotesWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.note_txt = ''
        self.initUI()

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

        # TIME
        self.time_lbl = ttk.Label(self.main_frame, text='Time:')
        self.time_lbl.pack(side='top', fill='both', expand=True)
        self.time_entry = tk.Entry(self.main_frame)  # needs to be tk since ttk doesn't have bg colors...
        self.time_entry.pack(side='top', fill='both', expand=True)

        # TYPE
        self.type_lbl = ttk.Label(self.main_frame, text='Type:')
        self.type_lbl.pack(side='top', fill='both', expand=True)

        # TAG
        self.tags_lbl = ttk.Label(self.main_frame, text='Tags:')
        self.tags_lbl.pack(side='top', fill='both', expand=True)

        # CONTENT
        self.content_lbl = ttk.Label(self.main_frame, text='Content:')
        self.content_lbl.pack(side='top', fill='both', expand=True)

        self.content_text = tk.Text(self.main_frame)
        self.content_text.insert('1.0', self.note_txt)
        self.content_text.pack(side='top', fill='both', expand=True)

        # COMMENTS
        self.comment_lbl = ttk.Label(self.main_frame, text='Comment:')
        self.comment_lbl.pack(side='top', fill='both', expand=True)

        self.comment_text = tk.Text(self.main_frame)
        self.comment_text.insert('1.0', self.note_txt)
        self.comment_text.pack(side='top', fill='both', expand=True)

        # BUTTONS
        self.buttons_down = tk.Frame(self)
        self.buttons_down.grid(row=1, column=0, sticky='nsew', columnspan=2)
        # self.buttons_down.pack(side='top', fill='both', expand=True)
        self.buttons_down.grid_rowconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(1, weight=1)

        self.savebtn = ttk.Button(self.buttons_down, text='Save')
        self.savebtn.grid(row=0, column=0, sticky='nswe')

        self.closebtn = ttk.Button(self.buttons_down, text='Close')
        self.closebtn.grid(row=0, column=1, sticky='nswe')

        main_frame_id = self.canvas.create_window(0, 0, anchor='nw', window=self.main_frame)
        self.main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        def on_canvas_configure(event):
            width = event.width
            self.canvas.itemconfigure(main_frame_id, width=width)
        self.canvas.bind('<Configure>', on_canvas_configure)
