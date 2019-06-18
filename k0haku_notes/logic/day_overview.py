from datetime import datetime

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager

import logic.models as m



class DayOverviewController:
    def __init__(self):
        self.db = get_db_manager()
        
        self.note_list = m.NoteListModel([])
    
    def init_values(self):
        self.load()
       
    def convert_note(self, note_dict):
        # move convert logic to db_manager, duplicates with another method in note.py
        # TODO: make time return timestamp
        note_dict['time'] = datetime.strptime(note_dict['time'], "%Y-%m-%dT%H:%M:%SZ")

        types = note_dict['types']
        if types != []: 
            note_dict['types'] = types[0] if isinstance(types, list) else types
            note_dict['types'] = self.db.get_type_by_id(note_dict['types'])['name']

        note_dict['tags'] = self.db.get_tags_by_ids(note_dict['tags'])

    def load(self):
        note_list = self.db.notes.list().json()
        for note in note_list:
            self.convert_note(note)
            self.note_list.append(self.get_note_values(note))

    def delete(self, index):
        id = self.note_list.get_by(index)[4]
        self.db.notes.destroy(id)

    def get_selected_note_id(self, index):
        return self.note_list.get_by(index)[4]  # very ugly
    
    def add_note(self, note):
        self.convert_note(note)
        self.note_list.append(self.get_note_values(note))
        
    def edit_note(self, note):
        self.convert_note(note)
        for i, val in enumerate(self.note_list.var.data):  # maybe enumerate or similar
            if val[4] == note['id']:
                self.note_list.set_by(i, self.get_note_values(note))

    def get_note_values(self, note):
        return (note['time'], note['content'], note['types'], note['tags'], note['id'])