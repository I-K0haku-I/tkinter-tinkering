from app.frames import AddNotesWindow, StartPage, NoteOverview

# TODO: instead of classes use strings
# import that string object in the main file and in all frames
# show_frame now takes a string and translates it from a string to a class
class ViewRefs(object):
    START = StartPage
    NOTES_OVERVIEW = NoteOverview
    EDIT_NOTE = AddNotesWindow