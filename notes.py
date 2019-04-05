import tkinter as tk
import os
from tkinter import ttk

from frames import AddNotesWindow, NoteOverview

DEFAULT_NOTES_PATH = '.\\notes\\'

def add_file():
    popup = tk.Toplevel()

    popup.title('test')
    label = ttk.Label(popup, text='test')
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='okay', command=popup.destroy)
    B1.pack()


class NotesApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('TEST')

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Add file...', command=lambda: add_file)
        filemenu.add_command(label='Settings', command=lambda: print('lul'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        test = tk.Menu(menubar, tearoff=0)
        test.add_command(label='Exit', command=quit)
        test.add_checkbutton(label='check')
        test.add_separator()
        test.add_radiobutton(label='radio')
        test.add_radiobutton(label='radio2')
        filemenu.add_cascade(label='TEST', menu=test)
        menubar.add_cascade(label='Stuff...', menu=filemenu)
        
        self.config(menu=menubar)

        self.notes_path = tk.StringVar(self, DEFAULT_NOTES_PATH)
        self.selected_file = tk.StringVar(self)

        self.frames = {}
        frame_list = (StartPage, NoteOverview)
        for F in frame_list:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if frame is not None:
            frame.destroy()
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames[cont] = frame
    
    def get_file_path(self):
        return self.notes_path.get() + self.selected_file.get()
    
    # TODO: might remove
    def set_var(self, cont, name, val):
        if hasattr(self.frames[cont], name):
            setattr(self.frames[cont], name, val)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text='Hello World')
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text='ACTUALLY Start App', command=lambda: controller.show_frame(NoteOverview))
        button.pack()


def print_text(text):
    print(text)

app = NotesApp()
app.geometry('640x480')
app.mainloop()
app.destroy()
