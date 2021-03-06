import asyncio
from datetime import datetime, date, timedelta

from base_api_connector import AsDictObject
from utils.db_manager import get_db_manager

import logic.models as m


class DayOverviewController:
    def __init__(self):
        self.db = get_db_manager()
        self.cached_dates = {}
        self.clear_list_func = lambda: None
        header_sizes = (0.15, 0.5, 0.075, 0.0625, 0.28)
        self.header = tuple(zip(m.NOTE_COL_NAMES, header_sizes))

        self.note_list = m.NoteListModel([])
        self.date = m.DateModel(0)

    def init_values(self):
        # self.db.get_tags(refresh=True)
        self.date.set(date.today())
        # self.load_other()
        self.load_note_list()
    
    # def load_other(self):
    #     asyncio.create_task(self.db.load_types())

    def refresh(self):
        self.cached_dates.pop(self.date.get(), None)
        self.load_note_list()

    def load_note_list(self):
        if self.date.get() not in self.cached_dates.keys():
            self.cached_dates[self.date.get()] = None
            asyncio.create_task(self.load_note_list_async())  # might give in date
            return

        if self.cached_dates[self.date.get()] is None:  # currently retreiving data so should not do anything
            return
        self.set_note_list()

    def load_note_list_normal(self):
        date = self.date.get()
        new_note_list_resp = self.db.notes.list(params={'date': date})
        new_note_list = new_note_list_resp.json()
        new_note_list = [self.db.convert_note(note) for note in new_note_list]
        new_note_list.sort(key=lambda x: x['time'])
        self.cached_dates[date] = new_note_list

        self.load_note_list()

    async def load_note_list_async(self):
        date = self.date.get()
        new_note_list_resp = await self.db.notes.list(params={'date': date})
        if new_note_list_resp.content_type != 'application/json':
            print(f'Error: Status code: {new_note_list_resp.status}')
            print('This is the body:')
            print(await new_note_list_resp.text())
            print('Skipping...')
            return
        new_note_list = await new_note_list_resp.json()
        new_note_list = [self.db.convert_note(note) for note in new_note_list]
        new_note_list.sort(key=lambda x: x['time'])
        self.cached_dates[date] = new_note_list

        self.load_note_list()

    def set_note_list(self):
        new_note_lst = self.cached_dates[self.date.get()]
        self.clear_notes()
        for note in new_note_lst:
            # note = self.db.convert_note(note)
            self.note_list.add_item(self.convert_to_values(note))

    def next_day(self):
        self.clear_notes()
        self.date.set(self.date.get(as_string=False) + timedelta(days=1))
        self.load_note_list()

    def prev_day(self):
        self.clear_notes()
        self.date.set(self.date.get(as_string=False) - timedelta(days=1))
        self.load_note_list()

    def delete(self, index):
        return asyncio.create_task(self.delete_async(index))

    async def delete_async(self, index):
        id = self.note_list.get_by(index).id
        r = await self.db.notes.destroy(id)
        if r.status in (204,):
            note = self.note_list.pop(index)
            date = note[0].strftime('%Y-%m-%d')
            del self.cached_dates[date][index]
            return True
        return False

    def clear_notes(self):
        self.clear_list_func()
        self.note_list.set([])

    def get_selected_note_id(self, index):
        return self.note_list.get_by(index).id

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

        date = new_note['time'].strftime('%Y-%m-%d')
        if date not in self.cached_dates.keys():
            self.cached_dates[date] = []

        self.cached_dates[date].insert(new_index, new_note)
        self.set_note_list()

        # self.note_list.add_item(self.convert_to_values(new_note), index=new_index)

    def edit_note(self, note):
        note = self.db.convert_note(note)
          # looks at this, we are directly accessing the var.data here
          # it would be better if it could access the class and iterate over it directly
          # it would be better overall, if we would access it not by id but by some other more clear interface too
          # below we would not need to convert the note to values like that for example.
        for i, val in enumerate(self.note_list.var.data):
            if val.id == note['id']:
                self.note_list.set_by(i, self.convert_to_values(note))
                self.note_list.move_item(i, self.get_new_pos(note))
                date = note['time'].strftime('%Y-%m-%d')
                self.cached_dates[date][i] = note
                break

    def convert_to_values(self, note):  # TODO: feels like it should be in its own model, in NoteListModel?
        duration = m.DurationModel(note['duration']).to_simple_str()
        duration_unit = 'HOURS' if '.' in duration else 'MINS'
        return m.NoteRow(note['time'], note['content'], duration, duration_unit, note['tags'], note['id'])
