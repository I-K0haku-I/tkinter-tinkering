
from tkinter import Tk, W, E, N, S, BOTH, Text, END,Toplevel
from tkinter.ttk import Frame, Button, Entry, Label


class AddNotesWindow(Frame):

    def __init__(self, parent, controller):
        print('created!!!!!!!!!!!!!!!!!!!!!!!!')
        super().__init__(parent)
        self.save_callback = save_to_file
        self.file_path = controller.get_file_path()
        self.file = open(self.file_path)
        self.note_txt = self.file.read()
        self.initUI()

    def set_save_callback(self, callback):
        self.save_callback = callback

    def set_close_callback(self, callback):
        self.close_callback = callback

    def initUI(self):
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.lbl = Label(self, text='Input:')
        self.lbl.grid(sticky=W, pady=4, padx=5)

        self.txtarea = Text(self)
        self.txtarea.insert('1.0', self.note_txt)
        self.txtarea.grid(row=1, column=0, columnspan=2,
                          rowspan=4, padx=5, sticky=E+W+S+N)

        self.savebtn = Button(self, text='Save', command=self.save)
        self.savebtn.grid(row=5, column=0, sticky=N+W+S)

        self.closebtn = Button(self, text='Close', command=self.close)
        self.closebtn.grid(row=5, column=1, sticky=N+E+S)

    def save(self):
        if self.save_callback:
            text = self.txtarea.get('1.0', 'end-1c')
            self.save_callback(text)

    def close(self):
        self.destroy()


# TODO: add logic for saving stuff to files
def save_to_file(file, text):
    print(text)


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
