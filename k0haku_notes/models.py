import tkinter as tk

from base_api_connector import AsDictObject


class Model():

    def get_fields(self):
        if not hasattr(self, '_tk_var_fields'):
            attrs = dir(self)
            fields = [(field_name, attrs.pop(field_name))
                      for field_name, obj in list(attrs.items())
                      if isinstance(obj, tk.Variable)]
            setattr(self, '_tk_var_fields', fields)
        return dict(self._tk_var_fields)

    def as_dict(self):
        return {key: value for key, value in self.get_fields().items()}
    

class IntField():




class Notes(Model):
    resource = 'notes'

    created = tk.IntVar()
    updated = tk.IntVar()
    content = tk.StringVar()
    comments = tk.StringVar()
    types = tk.Variable()
    tags = tk.Variable()
    time = tk.IntVar()


class Tags(Model):
    resource = 'tags'

    name = tk.StringVar()
    description = tk.StringVar()
    color = tk.StringVar()


class Types(Model):
    resource = 'types'

    name = tk.StringVar()
    description = tk.StringVar()
