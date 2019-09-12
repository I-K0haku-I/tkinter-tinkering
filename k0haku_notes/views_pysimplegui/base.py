import PySimpleGUI as sg

def test():
    return [sg.Text('test')]

num_test = 1

def create_layout():
    return [test() for i in range(num_test)] + [[sg.Exit()]]

# keep_on_top to true, for floating above everything, could make a constantly open notepad :thinking:
def create_window(layout):
    return sg.Window('Notes App', layout, finalize=True, no_titlebar=False, grab_anywhere=True)

window = create_window(create_layout())

while True:
    event, values = window.read(timeout=3000)
    print(event)
    if event in (None, 'Exit'):
        break
    if event == sg.TIMEOUT_KEY:
        print('WE ARE REFRESHING')
        window.close()
        num_test += 1
        window1 = create_window(create_layout())
        window = window1

window.close()