from datetime import datetime

from base_api_connector import GenericAPIConnector, APIResource


class NotesDBConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    notes = APIResource('all')
    tags = APIResource('all')
    types = APIResource('all')


db_manager_singleton = None

USE_CACHE = True


class DBManager:
    def __init__(self):
        self.conn = NotesDBConnector()
        self._tags = None
        self._types = None

    def get_tags(self, refresh=False):
        if self._tags is None or refresh or not USE_CACHE:
            self._tags = self.conn.tags.list().json()
        return self._tags

    def get_type(self, refresh=False):
        # I don't know if this is a good idea to optimize so much, I could just request new data every time
        # maybe except if there is no connection?
        if self._types is None or refresh or not USE_CACHE:
            self._types = self.conn.types.list().json()
        return self._types

    def get_type_by_id(self, id):
        for type in self.get_type():
            if type['id'] == id:
                return type['name']

    def get_type_id(self, type_str):
        if not type_str:
            return ''

        for type in self.get_type():
            if type['name'] == type_str:
                return type['id']
        else:
            r = self.conn.types.create(dict(name=type_str))
            if r.ok:
                self._types.append(r.json())
                return r.json()['id']
            else:
                print(f'Failed to create type: {type_str}')

    def get_tags_ids(self, str_list):
        return list(self._tags_convert_string_to_ids(str_list))

    def _tags_convert_string_to_ids(self, str_list):
        if not str_list:
            return []

        for name in str_list:
            for tag in self.get_tags():
                if tag['name'] == name:
                    yield tag['id']
                    break
            else:
                r = self.conn.tags.create(dict(name=name))
                if r.ok:
                    self._tags.append(r.json())
                    yield r.json()['id']
                else:
                    print(f'Failed to create tag: {name}')

    def get_tags_by_ids(self, id_list):
        return list(self._tags_convert_ids_to_string(id_list))

    def _tags_convert_ids_to_string(self, id_list):
        if not id_list:
            return []

        for id in id_list:
            for tag in self.get_tags():
                if tag['id'] == id:
                    yield tag['name']
                    continue

    def convert_note(self, note_dict):
        # move convert logic to db_manager, duplicates with another method in note.py
        # TODO: make time return timestamp

        new_note_dict = note_dict.copy()

        new_note_dict['time'] = datetime.strptime(new_note_dict['time'], "%Y-%m-%dT%H:%M:%SZ")
        new_note_dict['type'] = self.get_type_by_id(new_note_dict['type']) if new_note_dict['type'] else ''
        new_note_dict['tags'] = self.get_tags_by_ids(new_note_dict['tags'])

        return new_note_dict

    def __getattr__(self, attr):
        return getattr(self.conn, attr)


def get_db_manager():
    global db_manager_singleton
    if db_manager_singleton is None:
        db_manager_singleton = DBManager()
    return db_manager_singleton