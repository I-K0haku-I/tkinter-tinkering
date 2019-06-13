from datetime import datetime

import logic.models as m

class AddNotesAdapter:
    def __init__(self, id=None):
        self.id = id
        # self.model = m.NoteModel()
        # self.on_timestamp_validate = lambda bool: None
        
        self.timestamp = m.TimeModel(0)
        self.selected_type = m.SelectedTypeModel('')
        self.types_list = m.TypesListModel([])
        self.selected_tags_list = m.SelectedTagsListModel([])
        self.content = m.ContentModel('')
        self.comment = m.CommentModel('')
        # TODO: now get save and load in here as well


    def init_values(self):
        self.timestamp.set(datetime.today())
        self.types_list.set(['test', 'test2'])

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