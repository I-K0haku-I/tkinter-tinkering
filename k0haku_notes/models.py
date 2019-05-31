import tkinter as tk
from datetime import datetime

from base_api_connector import AsDictObject

from utils.notes_db_connector import NotesDBConnector


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


essential_data = None


class DBManager:
    def __init__(self):
        self.conn = NotesDBConnector()
        self._tags = None
        self._types = None

    def get_tags(self):
        if self._tags is None:
            self._tags = self.conn.tags.list().json()
        return self._tags
    
    def get_types(self):
        if self._types is None:
            self._types = self.conn.types.list().json()
        return self._types
        
    def get_type_by_id(self, id):
        for type in self.get_types():
            if type['id'] == id:
                return type

    def get_type_id(self, str):
        # TODO: add create if doesn't exist
        for type in self.get_types():
            if type['name'] == str:
                return type['id']

    def get_tags_ids(self, str_list):
        return list(self._tags_convert_string_to_ids(str_list))
    
    def _tags_convert_string_to_ids(self, str_list):
        for str in str_list:
            for tag in self.get_tags():
                if tag['name'] == str:
                    yield tag['id']
                    continue

    def get_tags_by_ids(self, id_list):
        return list(self._tags_convert_ids_to_string(id_list))

    def _tags_convert_ids_to_string(self, id_list):
        for id in id_list:
            for tag in self.get_tags():
                if tag['id'] == id:
                    yield tag['name']
                    continue

    def __getattr__(self, attr):
        return getattr(self.conn, attr)


def get_db_manager():
    global essential_data
    if essential_data is None:
        essential_data = DBManager()
    return essential_data


class NoteObject(AsDictObject): # TODO: remember to update asdictobject in the other module
    time = datetime.now().timestamp()
    content = 'Placeholder'
    detail = 'Placeholder'
    types = []
    tags = []


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
        new_time = datetime.strptime(note_dict['time'], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        self.timestamp.set(new_time) 

        type_ids = note_dict['types']
        new_selected_type = self.db_manager.get_type_by_id(type_ids[0])['name']
        self.selected_type.set(new_selected_type)

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
