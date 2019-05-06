from tkinter import ttk
import tkinter as tk
from tkinter import W, E, N, S


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
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(5, pad=7)

        self.lbl = ttk.Label(self, text='Input:')
        self.lbl.grid(sticky=W, pady=4, padx=5)

        self.txtarea = tk.Text(self)
        self.txtarea.insert('1.0', self.note_txt)
        self.txtarea.grid(row=1, column=0, columnspan=2,
                          rowspan=4, padx=5, sticky=E+W+S+N)

        self.grid_rowconfigure(5, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.buttons_down = tk.Frame(self)
        self.buttons_down.grid(row=5, column=0, columnspan=2, sticky=N+E+S+W)
        self.buttons_down.grid_rowconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(0, weight=1)
        self.buttons_down.grid_columnconfigure(1, weight=1)

        self.savebtn = ttk.Button(
            self.buttons_down, text='Save', command=self.save)
        self.savebtn.grid(row=0, column=0, sticky=N+W+E+S)

        self.closebtn = ttk.Button(
            self.buttons_down, text='Close', command=self.close)
        self.closebtn.grid(row=0, column=1, sticky=N+E+W+S)

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
