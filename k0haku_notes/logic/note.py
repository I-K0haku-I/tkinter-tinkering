from datetime import datetime

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager

import logic.models as m


class NoteObject(AsDictObject): # TODO: remember to update asdictobject in the other module
    time = datetime.now().timestamp()
    content = 'Placeholder'
    detail = 'Placeholder'
    types = []
    tags = []


class AddNotesAdapter:
    def __init__(self, id=None):
        self.id = id
        self.db_manager = get_db_manager()
        # self.model = m.NoteModel()
        # self.on_timestamp_validate = lambda bool: None
        
        self.timestamp = m.TimeModel(0)
        self.selected_type = m.SelectedTypeModel('')
        self.types_list = m.TypesListModel([])
        self.selected_tags_list = m.SelectedTagsListModel([])
        self.content = m.ContentModel('')
        self.comment = m.CommentModel('')

    def init_values(self):
        self.timestamp.set(datetime.now())
        self.types_list.set(['test', 'test2'])

        if self.id is not None:
            self.load()
    
    def convert_note(self, note_dict):
        # move convert logic to db_manager
        # TODO: make time return timestamp
        note_dict['time'] = datetime.strptime(note_dict['time'], "%Y-%m-%dT%H:%M:%SZ")

        types = note_dict['types']
        if types != []: 
            note_dict['types'] = types[0] if isinstance(types, list) else types
            note_dict['types'] = self.db_manager.get_type_by_id(note_dict['types'])['name']

        note_dict['tags'] = self.db_manager.get_tags_by_ids(note_dict)

    def load(self):
        r = self.db_manager.notes.retrieve(self.id)
        note_dict = r.json()
        if r.status_code != 200:
            return
        
        self.convert_note(note_dict)

        self.timestamp.set(note_dict['time']) 
        self.selected_type.set(note_dict['types'])
        self.selected_tags_list.set(note_dict['tags'])
        self.content.set(note_dict['content'])
        self.comment.set(note_dict['detail'])

    def store(self):
        note = NoteObject()
        note.time = datetime.strftime(self.timestamp.get(), "%Y-%m-%dT%H:%M:%SZ")
        note.content = self.content.get()
        note.detail = self.comment.get()
        note.types = [self.db_manager.get_type_id(self.selected_type.get())]
        note.tags = self.db_manager.get_tags_ids(self.selected_tags_list.get())

        if self.id:
            r = self.db_manager.notes.update(self.id, note)
        else:
            r = self.db_manager.notes.create(note)
        return r

    # def init_values(self):
    #     self.set_timestamp(datetime.today())
    #     self.model.types_list.set(['test', 'test2'])
    #     if self.id:
    #         self.model.load(self.id)

#     def save_note(self):
#         # print(self.model.timestamp.get())
#         # print(self.note_form.time_var.get())
#         # print(self.model.selected_type.get())
#         print(self.model)
#         self.model.store(self.id)

# # subscribe functions
# # used to change view when model changes
#     def subscribe_to_content(self, func):
#         self.model.content.add_callback(func)

#     def subscribe_to_timestamp(self, func):
#         def func_as_str(timestamp):
#             func(self.model.convert_to_datetime_str(timestamp))
#         self.model.timestamp.add_callback(func_as_str)

#     def subscribe_to_selected_type(self, func):
#         self.model.selected_type.add_callback(func)

#     def subscribe_to_type_list(self, func):
#         self.model.types_list.add_callback(func)

#     def subscribe_to_tags(self, func):
#         def func_as_str(tags_list):
#             func(','.join(tags_list))
#         self.model.selected_tags_list.add_callback(func_as_str)

#     def subscribe_to_comment(self, func):
#         self.model.comment.add_callback(func)

# # set funcitons
# # used to set model variables when view changes
#     def set_content(self, content_str):
#         self.model.content.set(content_str)

#     def set_timestamp(self, datetime_string):
#         try:
#             time = self.model.convert_to_timestamp(datetime_string)
#             self.model.timestamp.set(time)
#             self.on_timestamp_validate(True)
#         except:
#             self.on_timestamp_validate(False)

#     def set_selected_type(self, type_string):
#         self.model.selected_type.set(type_string)
#         # TODO: could send back whether type already exists or not and then display it

#     def set_tags(self, tags_str):
#         new_tags_list = [tag.strip() for tag in tags_str.split(',')]
#         self.model.selected_tags_list.set(new_tags_list)

#     def set_comment(self, comment_str):
#         self.model.comment.set(comment_str)