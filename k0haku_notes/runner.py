import tkinter as tk
from tkinter import ttk

from views_tk.base import RootNotesApp


class NotesAppRunner:
    def __init__(self):
        view = RootNotesApp()
        view.start()


if __name__ == "__main__":
    app = NotesAppRunner()
