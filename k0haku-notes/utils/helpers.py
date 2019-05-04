import tkinter as tk

from frames.add_notes import AddNotesWindow, AddNotesWindowController
from frames.start_page import StartPage, StartPageController


VIEW_TO_CONTROLLER = {
    StartPage: StartPageController,
    AddNotesWindow: AddNotesWindowController
}

class FrameHolder(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(side='top', fill='both', expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_controller = controller
        self.controllers = {}
        self.selected_frame = None

    def add(self, View):
        self.controllers[View] = VIEW_TO_CONTROLLER[View](self, self.main_controller)
        self.controllers[View].view.grid(row=0, column=0, sticky='nsew')

    def show(self, View):
        self.controllers.get(View).view.tkraise()

        # frame = getattr(self.controllers.get(View), 'view', None)
        # if frame is not None:
        #     frame.destroy()
        # frame = View(self, self.main_controller)
        # frame.grid(row=0, column=0, sticky='nsew')
        # self.frames[View] = frame