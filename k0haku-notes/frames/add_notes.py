from tkinter import ttk
import tkinter as tk
from tkinter import W, E, N, S

from utils.helpers import AutoScrollbar

class AddNotesWindowController:
    def __init__(self, view, controller):
        self.parent_controller = controller
        self.view = view


class AddNotesWindow(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.save_callback = save_to_file
        # self.file_path = controller.get_file_path()
        # self.file = open(self.file_path)
        # self.note_txt = self.file.read()
        self.note_txt = ''
        self.initUI()

    def set_save_callback(self, callback):
        self.save_callback = callback

    def set_close_callback(self, callback):
        self.close_callback = callback

    def initUI(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollbar = AutoScrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.scrollbar.config(command=self.canvas.yview)

        self.canvased_frame = tk.Frame(self.canvas)
        self.canvased_frame.grid_rowconfigure(1, weight=1)
        self.canvased_frame.grid_columnconfigure(1, weight=1)

        self.time_lbl = ttk.Label(self.canvased_frame, text='Time:')
        self.time_lbl.pack(side='top', fill='both', expand=True)
    
        self.type_lbl = ttk.Label(self.canvased_frame, text='Type:')
        self.type_lbl.pack(side='top', fill='both', expand=True)

        self.tags_lbl = ttk.Label(self.canvased_frame, text='Tags:')
        self.tags_lbl.pack(side='top', fill='both', expand=True)

        self.content_lbl = ttk.Label(self.canvased_frame, text='Content:')
        self.content_lbl.pack(side='top', fill='both', expand=True)

        self.content_text = tk.Text(self.canvased_frame)
        self.content_text.insert('1.0', self.note_txt)
        self.content_text.pack(side='top', fill='both', expand=True)

        self.comment_lbl = ttk.Label(self.canvased_frame, text='Comment:')
        self.comment_lbl.pack(side='top', fill='both', expand=True)

        self.comment_text = tk.Text(self.canvased_frame)
        self.comment_text.insert('1.0', self.note_txt)
        self.comment_text.pack(side='top', fill='both', expand=True)

        self.buttons_down = tk.Frame(self.canvased_frame)
        self.buttons_down.pack(side='top', fill='both', expand=True)
        self.buttons_down.grid_rowconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(1, weight=1)

        self.savebtn = ttk.Button(self.buttons_down, text='Save', command=self.save)
        self.savebtn.grid(row=0, column=0, sticky=N+W+E+S)

        self.closebtn = ttk.Button(self.buttons_down, text='Close', command=self.close)
        self.closebtn.grid(row=0, column=1, sticky=N+E+W+S)

        self.canvas.create_window(0, 0, anchor='nw', window=self.canvased_frame)
        self.canvased_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))


    def save(self):
        if self.save_callback:
            text = self.txtarea.get('1.0', 'end-1c')
            self.save_callback(self.file_path, text)

    def close(self):
        self.destroy()


# TODO: add logic for saving stuff to files
def save_to_file(file, text):
    print('TODO: implement saving text to file')


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
