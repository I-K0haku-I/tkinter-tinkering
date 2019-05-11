from base_api_connector import GenericAPIConnector

class NotesDBConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    resource_config = {
        'notes': {
            'commands': 'all',
        },
        'tags': {
            'commands': 'all',
        },
        'types': {
            'commands': 'all',
        }
    }
