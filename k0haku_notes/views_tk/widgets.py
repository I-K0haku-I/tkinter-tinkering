import tkinter as tk
import tkinter.ttk as ttk


class FrameHolder(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(side='top', fill='both', expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.views = {}
        self.selected_frame = None

    def add(self, View):
        view = View(self)
        view.grid(row=0, column=0, sticky='nsew')
        self.views[View] = view
        return view


class AutoScrollbar(tk.Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")

# TODO: add a scrollable frame in here too


class ScrollableFrame(tk.Frame):
    def __init__(self, parent=None, scrollbar=None, *args, **kwargs):

        canvas = tk.Canvas(parent, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(-1*int(event.delta/120), 'units'))

        scrollbar.config(command=canvas.yview)

        super().__init__(canvas, *args, **kwargs)
        self.pack(side='top', fill='both', expand=True)

        main_frame_id = canvas.create_window(0, 0, anchor='nw', window=self)

        def on_canvas_configure(event):
            width = event.width
            canvas.itemconfigure(main_frame_id, width=width)
        canvas.bind('<Configure>', on_canvas_configure)

        self.canvas = canvas

    def grid(self, cnf={}, **kw):
        self.canvas.grid(cnf, **kw)

    def init_scrollbar(self):
        '''Start scrollbar after assigning elements to this frame
        '''
        self.update_idletasks()  # wait for render of windows
        self.canvas.config(scrollregion=self.canvas.bbox('all'))


# used in note form
# base for a field which is a label + variable that gets bound to another tk element
class FieldFrame(tk.Frame):
    def __init__(self, parent, label_text='', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        label = ttk.Label(self, text=label_text)
        label.pack(side='top', fill='both', expand=True)

        var = tk.StringVar(self)
        self.on_write_func = None
        var.trace_add('write', lambda *args: self.on_write_func())

        self.label = label
        self.var = var

    def subscribe_to_var(self, func):
        self.on_write_func = lambda: func(self.var.get())

    def set_var(self, new_comment):
        self.var.set(new_comment)


class EntryField(FieldFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        entry = tk.Entry(self, textvariable=self.var)
        entry.pack(side='top', fill='both', expand=True)

        self.entry = entry


class TimeField(EntryField):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def subscribe_to_var(self, func):
        self.on_write_func = self.set_validation_color(func)

    def set_validation_color(self, func):
        def wrapper():
            is_success = func(self.var.get())
            if is_success:
                self.entry.config(bg='white')
            else:
                self.entry.config(bg='red')
        return wrapper


class ComboboxField(FieldFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        combobox = ttk.Combobox(self, textvariable=self.var)
        combobox.pack(side='top', fill='both', expand=True)

        self.combobox = combobox

    def set_dropdown(self, values):  # can't do assignmnents in lambadas so have to do this...
        self.combobox['values'] = values


class TextField(FieldFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        text = tk.Text(self, height=20)
        text.bind('<KeyRelease>', lambda e: self.var.set(e.widget.get('1.0', 'end-1c')))
        text.pack(side='top', fill='both', expand=True)

        self.text = text
