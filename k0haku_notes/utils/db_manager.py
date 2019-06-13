from base_api_connector import GenericAPIConnector, APIResource


class NotesDBConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    notes = APIResource('all')
    tags = APIResource('all')
    types = APIResource('all')


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

