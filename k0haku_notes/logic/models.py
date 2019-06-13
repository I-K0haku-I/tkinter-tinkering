import tkinter as tk
from datetime import datetime

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager


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


class NoteObject(AsDictObject): # TODO: remember to update asdictobject in the other module
    time = datetime.now().timestamp()
    content = 'Placeholder'
    detail = 'Placeholder'
    types = []
    tags = []


class BaseModel:
    def __init__(self, init_value):
        self.var = ObservableVar(init_value)
    
    def get(self):
        return self.var.get()
    
    def set(self, value):
        return self.var.set(value)
    
    def on_change(self, func):
        self.var.add_callback(func)


class ListBaseModel(BaseModel):  # might do some try blocks to make sure it's a list
    def append(self, value):
        self.var.data.append(value) 


class TimeModel(BaseModel):
    def get(self, as_datetime=False):
        if as_datetime:
            return self.timestamp_to_datetime(self.var.get())
        else:
            return str(self.var.get())
    
    def timestamp_to_datetime(self, value):
        return str(datetime.fromtimestamp(value))[:-3]
    
    def set(self, iso_time, on_timestamp_validate=lambda is_validated: None):
        try:
            time = datetime.fromisoformat(str(iso_time)).replace(microsecond=0, second=0).timestamp()
            self.var.set(time)
            on_timestamp_validate(True)
        except:
            on_timestamp_validate(False)

    def on_change(self, func):
        def wrapper(value):
            func(self.timestamp_to_datetime(value))
        self.var.add_callback(wrapper)


class SelectedTypeModel(BaseModel):
    pass


class TypesListModel(ListBaseModel):
    pass


class SelectedTagsListModel(ListBaseModel):
    def set(self, value):
        new_tags_list = [tag.strip() for tag in value.split(',')]
        super().set(new_tags_list)
    
    def on_change(self, func):
        def func_converted_as_comma_separated_str(value): 
            func(','.join(value))
        super().on_change(func_converted_as_comma_separated_str)


class ContentModel(BaseModel):
    pass


class CommentModel(BaseModel):
    pass


class NoteModel:
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

        self.db_manager = get_db_manager()

    def load(self, id):
        r = self.db_manager.notes.retrieve(id)
        note_dict = r.json()
        if r.status_code != 200:
            return

        # TODO: make time return timestamp
        # move convert logic to db_manager
        new_time = datetime.strptime(note_dict['time'], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        self.timestamp.set(new_time) 

        type_ids = note_dict['types']
        try:
            new_selected_type = self.db_manager.get_type_by_id(type_ids[0])['name']
            self.selected_type.set(new_selected_type)
        except:
            pass

        tag_ids = note_dict['tags']
        self.selected_tags_list.set(self.db_manager.get_tags_by_ids(tag_ids))
        
        content = note_dict['content']
        self.content.set(content)

        comment = note_dict['detail']
        self.comment.set(comment)

    def store(self, id):
        note = NoteObject()
        note.time = datetime.strftime(datetime.fromtimestamp(self.timestamp.get()), "%Y-%m-%dT%H:%M:%SZ")
        note.content = self.content.get()
        note.detail = self.comment.get()
        note.types = [self.db_manager.get_type_id(self.selected_type.get())]
        note.tags = self.db_manager.get_tags_ids(self.selected_tags_list.get())
        if id:
            r = self.db_manager.notes.update(id, note)
        else:
            r = self.db_manager.notes.create(note)
        return r

    def convert_to_datetime_str(self, timestamp):
        return str(datetime.fromtimestamp(timestamp))[:-3]

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
