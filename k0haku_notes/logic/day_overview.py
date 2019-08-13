from datetime import datetime, date, timedelta

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager

import logic.models as m


class DayOverviewController:
    def __init__(self):
        self.db = get_db_manager()
        self.clear_list_func = lambda: None

        self.note_list = m.NoteListModel([])
        self.date = m.DateModel(0)

    def init_values(self):
        # self.db.get_tags(refresh=True)
        # self.db.get_type(refresh=True)
        self.date.set(date.today())
        self.load_note_list()

    def load_note_list(self):
        new_note_list = self.db.notes.list(params={'date': self.date.get()}).json()
        new_note_list = [self.db.convert_note(note) for note in new_note_list]
        new_note_list.sort(key=lambda x: x['time'])

        self.clear_list_func()
        self.note_list.set([])
        for note in new_note_list:
            # note = self.db.convert_note(note)
            self.note_list.add_item(self.convert_to_values(note))
    
    def next_day(self):
        self.date.set(self.date.get(as_string=False) + timedelta(days=1))
        self.load_note_list()
    
    def prev_day(self):
        self.date.set(self.date.get(as_string=False) - timedelta(days=1))
        self.load_note_list()

    def delete(self, index):
        id = self.note_list.get_by(index)[4]
        r = self.db.notes.destroy(id)
        if r.ok:
            self.note_list.pop(index)
        return r.ok 

    def get_selected_note_id(self, index):
        return self.note_list.get_by(index)[4]  # very ugly, magic numbers could be removed to solve it

    def get_new_pos(self, new_note):
        i = -1
        for i, note in enumerate(self.note_list.get()):
            if note[0] > new_note['time']:
                return i
        else:
            return i + 1

    def add_note(self, new_note):
        new_note = self.db.convert_note(new_note)
        new_index = self.get_new_pos(new_note)
        self.note_list.add_item(self.convert_to_values(new_note), index=new_index)

    def edit_note(self, note):
        note = self.db.convert_note(note)
        for i, val in enumerate(self.note_list.var.data):
            if val[4] == note['id']:
                self.note_list.set_by(i, self.convert_to_values(note))
                self.note_list.move_item(i, self.get_new_pos(note))
                break

    def convert_to_values(self, note):
        return (note['time'], note['content'], note['type'], note['tags'], note['id'])
