import tkinter as tk
from datetime import datetime, date

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


class NoteObject(AsDictObject):  # TODO: remember to update asdictobject in the other module
    time = datetime.now().timestamp()
    content = 'Placeholder'
    detail = 'Placeholder'
    type = []
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
    def __init__(self, init_value):
        self.on_add_item_func = lambda value, index=None: None
        self.on_set_by_func = lambda index, value: None
        self.on_move_item_func = lambda old_index, new_index: None
        super().__init__(init_value)

    def get_by(self, index):  # maybe better with dunder methods
        return self.var.data[index]

    def set_by(self, index, value):  # dunder
        self.var.data[index] = value
        self.on_set_by_func(index, value)
        # self.on_append_func(value, index)  # rename, weird now

    def add_item_without_event(self, value, index=None):
        if index:
            self.var.data.insert(index, value)
        else:
            self.var.data.append(value)

    def add_item(self, value, index=None):  # ugly?
        self.add_item_without_event(value, index)
        self.on_add_item_func(value, index)

    def move_item(self, old_index, new_index):
        if new_index > old_index:  # removing old_index will make the target position (new_index) different because whole list moves
            new_index -= 1
        self.var.data.insert(new_index, self.var.data.pop(old_index))
        self.on_move_item_func(old_index, new_index)

    def pop(self, index):  # might use getattr instead
        return self.var.data.pop(index)

class TimeModel(BaseModel):
    def get(self, as_string=True):
        if as_string:
            return self.datetime_to_str(self.var.get())
        else:
            return self.var.data

    def datetime_to_str(self, value):
        return str(value)[:-3]

    def set_string(self, iso_time, on_timestamp_validate=lambda is_validated: None):
        try:
            time = datetime.fromisoformat(str(iso_time)).replace(microsecond=0, second=0)
            super().set(time)
            on_timestamp_validate(True)
        except:
            on_timestamp_validate(False)

    def on_change(self, func):
        def func_with_value_as_str(value):
            value = self.datetime_to_str(value)
            func(value)
        super().on_change(func_with_value_as_str)

class DateModel(BaseModel):
    def get(self, as_string=True):
        if as_string:
            return str(self.var.get())
        else:
            return self.var.data
    
    def set_string(self, iso_time):
        try:
            date_to_set = date.fromisoformat(str(iso_time))
            super().set(date_to_set)
        except:
            print('Could not convert time str to date:', iso_time)

class SelectedTypeModel(BaseModel):
    pass


class TypeListModel(ListBaseModel):
    pass


class SelectedTagsListModel(ListBaseModel):
    def set_string(self, value):
        if not value:
            super().set([])
        new_tags_list = [tag.strip() for tag in value.split(',')]
        super().set(new_tags_list)

    def on_change(self, func):
        def func_converted_as_comma_separated_str(value):
            func(','.join(value) if value else [])
        super().on_change(func_converted_as_comma_separated_str)


class ContentModel(BaseModel):
    pass


class CommentModel(BaseModel):
    pass


class NoteListModel(ListBaseModel):
    pass

# class NoteModel:
#     timestamp = None
#     selected_type = None
#     types_list = None
#     selected_tags_list = None
#     content = None
#     comment = None

#     def __init__(self):
#         self.timestamp = ObservableVar(0, 'timestamp')
#         self.types_list = ListObservableVar([], 'types')
#         self.selected_type = ObservableVar('', 'selected_type')
#         self.selected_tags_list = ListObservableVar([], 'selected_tags_list')
#         self.content = ObservableVar('', 'content')
#         self.comment = ObservableVar('', 'comment')

#         self.db_manager = get_db_manager()

#     def load(self, id):
#         r = self.db_manager.notes.retrieve(id)
#         note_dict = r.json()
#         if r.status_code != 200:
#             return

#         # TODO: make time return timestamp
#         # move convert logic to db_manager
#         new_time = datetime.strptime(note_dict['time'], "%Y-%m-%dT%H:%M:%SZ").timestamp()
#         self.timestamp.set(new_time)

#         type_ids = note_dict['types']
#         try:
#             new_selected_type = self.db_manager.get_type_by_id(type_ids[0])['name']
#             self.selected_type.set(new_selected_type)
#         except:
#             pass

#         tag_ids = note_dict['tags']
#         self.selected_tags_list.set(self.db_manager.get_tags_by_ids(tag_ids))

#         content = note_dict['content']
#         self.content.set(content)

#         comment = note_dict['detail']
#         self.comment.set(comment)

#     def store(self, id):
#         note = NoteObject()
#         note.time = datetime.strftime(datetime.fromtimestamp(self.timestamp.get()), "%Y-%m-%dT%H:%M:%SZ")
#         note.content = self.content.get()
#         note.detail = self.comment.get()
#         note.types = [self.db_manager.get_type_id(self.selected_type.get())]
#         note.tags = self.db_manager.get_tags_ids(self.selected_tags_list.get())
#         if id:
#             r = self.db_manager.notes.update(id, note)
#         else:
#             r = self.db_manager.notes.create(note)
#         return r

#     def convert_to_datetime_str(self, timestamp):
#         return str(datetime.fromtimestamp(timestamp))[:-3]

#     def convert_to_timestamp(self, datetime_string):
#         return datetime.fromisoformat(str(datetime_string)).replace(microsecond=0, second=0).timestamp()

#     def __repr__(self):
#         return (f"{self.timestamp}, {self.selected_type}"
#                 f", {self.selected_tags_list}, {self.content}"
#                 f", {self.comment}")


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
