from views_tk import AddNotesWindow, StartPage

# TODO: instead of classes use strings
# import that string object in the main file and in all frames
# show_frame now takes a string and translates it from a string to a class
class ViewRefs(object):
    START = StartPage
    EDIT_NOTE = AddNotesWindow