import asyncio
import datetime as dt

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager

import logic.models as m


class NoteObject(AsDictObject): # TODO: remember to update asdictobject in the other module
    time = dt.datetime.now().timestamp()
    duration = str(dt.time())
    content = 'Placeholder'
    detail = 'Placeholder'
    tags = []


class AddNotesAdapter:
    def __init__(self, id=None):
        self.id = id
        self.db_manager = get_db_manager()
        # self.model = m.NoteModel()
        # self.on_timestamp_validate = lambda bool: None
        
        self.timestamp = m.TimeModel(0)
        self.duration = m.DurationModel(0)
        self.selected_tags_list = m.SelectedTagsListModel([])
        self.content = m.ContentModel('')
        self.comment = m.CommentModel('')

    def init_values(self, time=None):
        self.timestamp.set(dt.datetime.now() if time is None else time)
        self.duration.set(dt.time())

        if self.id is not None:
            self.load()

    def load(self):
        asyncio.create_task(self.load_async())

    async def load_async(self):
        r = await self.db_manager.notes.retrieve(self.id)
        note_dict = await r.json()
        if r.status != 200:
            print(f'Couldn\' load when retreiving {self.id}')
            return
        
        note_dict = self.db_manager.convert_note(note_dict)

        self.timestamp.set(note_dict['time'])
        self.duration.set(note_dict['duration'])
        self.selected_tags_list.set(note_dict['tags'])
        self.content.set(note_dict['content'])
        self.comment.set(note_dict['detail'])

    def store(self):
        asyncio.create_task(self.store_async())
    
    async def store_async(self):
        # ideally, I would not need this, the note data should already be correct and I just have to iterate and get their value
        note = NoteObject()
        note.time = dt.datetime.strftime(self.timestamp.get(as_string=False), "%Y-%m-%dT%H:%M:%SZ")
        note.duration = self.duration.get()
        note.content = self.content.get()
        note.detail = self.comment.get()
        tags = self.selected_tags_list.get()
        note.tags = self.db_manager.get_tags_ids([] if not tags or tags == [''] else tags)

        if self.id:
            r = await self.db_manager.notes.update(self.id, note.as_dict())
        else:
            r = await self.db_manager.notes.create(note.as_dict())
        if r.status not in (200, 201):
            print(f"Could not save: {r.reason}. Status code: {r.status}")
            return
        data = await r.json()
        return data
    

    def store_normal(self):
        note = NoteObject()
        note.time = dt.datetime.strftime(self.timestamp.get(as_string=False), "%Y-%m-%dT%H:%M:%SZ")
        note.content = self.content.get()
        note.detail = self.comment.get()
        tags = self.selected_tags_list.get()
        note.tags = self.db_manager.get_tags_ids([] if not tags or tags == [''] else tags)

        if self.id:
            r = self.db_manager.notes.update(self.id, note.as_dict())  # TODO: use json here instead of data to keep empty lists
        else:
            r = self.db_manager.notes.create(note.as_dict())
        return r
    
    def calc_duration(self):
        start_time = self.timestamp.get(as_string=False)
        new_duration = dt.datetime.now() - start_time
        # convert from timedelta to time
        new_duration = (dt.datetime.min + new_duration).time()
        self.duration.set(new_duration)
        


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