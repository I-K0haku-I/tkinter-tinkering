from base_api_connector import GenericAPIConnector, APIResource

class NotesDBConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    notes = APIResource('all')
    tags = APIResource('all')
    types = APIResource('all')
