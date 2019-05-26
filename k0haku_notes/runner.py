import tkinter as tk
from tkinter import ttk

from models import TempModel
from views_tk.base import NotesAppView, RootNotesAppView
from views_tk.note_form import AddNotesView
from views_tk.start_page import StartPage
from views_tk.day_overview import DayOverview

class NotesAppRunner:
    def __init__(self):
        view = RootNotesAppView()
        view.start()

if __name__ == "__main__":
    app = NotesAppRunner()
