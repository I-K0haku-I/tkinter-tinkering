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
        # move convert logic to db_manager
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
            self.note_list.append((note['time'], note['content'], note['types'], note['tags']))

    def get_selected_note_id(self):
        return 3