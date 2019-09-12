import tkinter as tk
import asyncio
from tkinter import ttk
from .widgets import FrameHolder

from .note_form import AddNotesView
from .start_page import StartPage
from .day_overview_list import DayOverview


class RootNotesApp:
    def __init__(self):
        main_window = tk.Tk()

        day_overview_frame = DayOverview(main_window)
        day_overview_frame.pack(side='top', fill='both', expand=True)

        self.main_window = main_window
        self.main_frame = day_overview_frame
    
    def start(self):
        asyncio.run(self.run_tk())

    async def run_tk(self):
        self.main_frame.controller.init_values()
        try:
            while True:
                self.main_window.update()
                await asyncio.sleep(0.05)
        except tk.TclError as e:
            if 'application has been destroyed' not in e.args[0]:
                raise
        # self.main_window.mainloop()



# def create_popup(title='Popup', msg='', buttons=('OK',)):
#     popup = tk.Toplevel()
#     popup.title(title)
#     label = ttk.Label(popup, text=msg)
#     label.pack(side='top', fill='x', pady=10)
#     for b in buttons:
#         B1 = ttk.Button(popup, text=b, command=popup.destroy)
#         B1.pack()


# # This feels like a bad idea, I think I should just write out the menu in the menu
# SUBMENU_COMMANDS = {
#     'Add file...': lambda: create_popup(),
#     'Settings': lambda: print('lul'),
#     'Exit': quit
# }


# TODO not used anymore------------------------------------
# class NotesAppView(tk.Tk):
#     def __init__(self, controller, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.controller = controller

#         self.title('Notes')
#         self.geometry('640x500')

#         self.menubar = NotesAppMenu(self)
#         menu = self.menubar.subsubmenu
#         menu.entryconfigure(menu.index('Exit'), command=lambda: self.change_interior_to(StartPage))
#         menu = self.menubar.submenu
#         for name, command in controller.SUBMENU_COMMANDS.items():
#             menu.entryconfigure(menu.index(name), command=command)
#         self.config(menu=self.menubar)

#         self.frame = FrameHolder(self)
#         start_page = self.frame.add(StartPage)
#         add_notes = self.frame.add(AddNotesView)
#         day_overview = self.frame.add(DayOverview)

#         start_page.button.config(command=lambda: self.change_interior_to(AddNotesView))
#         start_page.button2.config(command=lambda: self.change_interior_to(DayOverview))
#         add_notes.closebtn.config(command=lambda: self.change_interior_to(StartPage))
#         day_overview.add_btn.config(command=lambda: self.open_add_note_window(DayOverview))

#     def change_interior_to(self, View):
#         self.frame.views.get(View).tkraise()

#     def get_interior(self, View):
#         return self.frame.views.get(View)

#     def open_add_note_window(self, return_View):
#         new_window = tk.Toplevel(self)
#         add_note = AddNotesView(new_window)
#         add_note.pack(side='top', fill='both', expand=True)
#         add_note.closebtn.config(command=new_window.destroy)

#     def start(self):
#         self.mainloop()


# class NotesAppMenu(tk.Menu):
#     def __init__(self, parent, *args, **kwargs):
#         controller = parent.controller
#         super().__init__(parent, *args, **kwargs)

#         self.submenu = tk.Menu(self, tearoff=0)
#         for name in controller.SUBMENU_COMMANDS.keys():
#             self.submenu.add_command(label=name)
#         self.submenu.insert_separator(2)

#         self.subsubmenu = tk.Menu(self.submenu, tearoff=0)

#         self.subsubmenu.add_command(label='Exit')
#         self.subsubmenu.add_checkbutton(label='check')
#         self.subsubmenu.add_separator()
#         self.subsubmenu.add_radiobutton(label='radio')
#         self.subsubmenu.add_radiobutton(label='radio2')

#         self.submenu.add_cascade(label='TEST', menu=self.subsubmenu)

#         self.add_cascade(label='Stuff...', menu=self.submenu)
#         self.add_cascade(label='Stuff2...', menu=self.submenu)
#         self.add_cascade(label='Stuff3...', menu=self.subsubmenu)
