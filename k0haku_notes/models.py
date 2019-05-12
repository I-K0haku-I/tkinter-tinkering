import tkinter as tk
from datetime import datetime

from base_api_connector import AsDictObject


class TempModel:
    timestamp = datetime.now().timestamp()
    timestamp_field = None
    is_convert_failed = False

    def __init__(self, parent):
        self.parent = parent
        self.time_string = tk.StringVar(parent.view)
        self.time_string.set(self.set_string_to_timestamp)
        self.time_string.trace_add('read', self.set_string_to_timestamp)
        self.time_string.trace_add('write', self.set_timestamp_to_string)

    def set_string_to_timestamp(self, *args):
        self.time_string.set(datetime.fromtimestamp(int(self.timestamp)))
    
    def set_timestamp_to_string(self, *args):
        try:
            self.timestamp = datetime.fromisoformat(self.time_string.get()).timestamp()
            self.timestamp_field.config(bg='white')
        except:
            self.timestamp_field.config(bg='red')


        

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
