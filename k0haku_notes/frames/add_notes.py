from tkinter import ttk
import tkinter as tk
from tkinter import W, E, N, S

from utils.helpers import AutoScrollbar


class AddNotesWindowController:
    def __init__(self, model, view, close_callback):
        self.file_path = 'test'  # controller.get_file_path()
        # self.file = open(self.file_path)
        # self.note_txt = self.file.read()
        self.save_callback = save_to_file

        self.model = model
        self.view = view
        self.view.savebtn.config(command=self.save)
        self.view.closebtn.config(command=close_callback)
        self.view.time_entry.config(textvariable=self.model.time)

    def save(self):
        if self.save_callback:
            text = self.view.content_text.get('1.0', 'end-1c')
            self.save_callback(self.file_path, text)

    def set_save_callback(self, callback):
        self.save_callback = callback

    def set_close_callback(self, callback):
        self.close_callback = callback


# TODO: add logic for saving stuff to files
def save_to_file(file, text):
    print('TODO: implement saving text to file')


class AddNotesWindow(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
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
        self.time_entry = ttk.Entry(self.main_frame)
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
        self.buttons_down = tk.Frame(self.main_frame)
        self.buttons_down.pack(side='top', fill='both', expand=True)
        self.buttons_down.grid_rowconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(1, weight=1)

        self.savebtn = ttk.Button(self.buttons_down, text='Save')
        self.savebtn.grid(row=0, column=0, sticky=N+W+E+S)

        self.closebtn = ttk.Button(self.buttons_down, text='Close')
        self.closebtn.grid(row=0, column=1, sticky=N+E+W+S)

        main_frame_id = self.canvas.create_window(0, 0, anchor='nw', window=self.main_frame)
        self.main_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        def on_canvas_configure(event):
            width = event.width
            self.canvas.itemconfigure(main_frame_id, width=width)
        self.canvas.bind('<Configure>', on_canvas_configure)


# def main():
# root = Tk()
# root.geometry("350x300+300+300")
# app = AddNotesWindow()
# app.set_save_callback(print_text)

# top = Toplevel()
# app2 = AddNotesWindow(master=top)
# app2.set_save_callback(print_text)

# root.mainloop()
# root.destroy()
