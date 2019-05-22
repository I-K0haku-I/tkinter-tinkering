import tkinter as tk
from datetime import datetime

from base_api_connector import AsDictObject

class ObservableVar:
    _callbacks = None  # can't initiate dict here because it will be the same for all ObservableVar instances for some reason
    
    def __init__(self, start_val=0, identity=None):
        self._callbacks = {} 
        self.identity = identity
        self.data = start_val
    
    def add_callback(self, callback):
        self._callbacks[callback] = 1

    def get(self):
        return self.data

    def set(self, value):
        self.data = value
        self._do_callbacks()
    
    def _do_callbacks(self):
        for func in self._callbacks:
            func(self.data)

    def __str__(self):
        return str(self.data)


class ListObservableVar(ObservableVar):
    def __init__(self, start_val=[], identity=None):
        if not isinstance(start_val, list):
            raise TypeError('Has to be a list.')
        super().__init__(start_val, identity)

    def append(self, value):
        self.data.append(value)


class TempModel:
    timestamp = None
    selected_type = None
    types_list = None
    selected_tags_list = None
    content = None
    comment = None

    def __init__(self):
        self.timestamp = ObservableVar(0, 'timestamp')
        self.types_list = ListObservableVar([], 'types')
        self.selected_type = ObservableVar('', 'selected_type')
        self.selected_tags_list = ListObservableVar([], 'selected_tags_list')
        self.content = ObservableVar('', 'content')
        self.comment = ObservableVar('', 'comment')

    def convert_to_timestamp(self, datetime_string):
        return datetime.fromisoformat(str(datetime_string)).replace(microsecond=0, second=0).timestamp()

    def __repr__(self):
        return (f"{self.timestamp}, {self.selected_type}"
                f", {self.selected_tags_list}, {self.content}"
                f", {self.comment}")

# class Model():
#     _tk_var_fields = None

#     def get_fields(self):
#         if not hasattr(self, '_tk_var_fields'):
#             attrs = dir(self)
#             fields = [(field_name, attrs.pop(field_name))
#                       for field_name, obj in list(attrs.items())
#                       if isinstance(obj, tk.Variable)]
#             setattr(self, '_tk_var_fields', fields)
#         return dict(self._tk_var_fields)

#     def as_dict(self):
#         return {key: value for key, value in self.get_fields().items()}


# class IntField():
#     pass


# class Notes(Model):
#     resource = 'notes'

#     created = tk.IntVar()
#     updated = tk.IntVar()
#     content = tk.StringVar()
#     comments = tk.StringVar()
#     types = tk.Variable()
#     tags = tk.Variable()
#     time = tk.IntVar()


# class Tags(Model):
#     resource = 'tags'

#     name = tk.StringVar()
#     description = tk.StringVar()
#     color = tk.StringVar()


# class Types(Model):
#     resource = 'types'

#     name = tk.StringVar()
#     description = tk.StringVar()
