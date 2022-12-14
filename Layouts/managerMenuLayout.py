import PySimpleGUI as sg


def open_manager_window():
    manager_menu_layout = [[sg.Text("Manager Menu")],
                           [sg.Text("Username :", size=(10, 1)),
                            sg.InputText('', size=(20, 1), key='input_username')],
                           [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                           [sg.Text("Secret Word :", size=(10, 1)),
                            sg.InputText('', size=(20, 1), key='input_secret_word')],
                           [sg.Text(size=(30, 1), key="Error")],
                           [sg.Submit(button_text="Confirm"),
                            sg.Exit(pad=((150, 0), (0, 0)))]]

    manager_menu_window = sg.Window("Manager Menu", manager_menu_layout, element_justification='c')
    while True:
        manager_menu_event, manager_menu_values = manager_menu_window.read()
        if manager_menu_event == "Confirm":
            input_username = manager_menu_values['input_username']
            input_ID = manager_menu_values['input_ID']
            input_secret_word = manager_menu_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                manager_menu_window["Error"].update("One or more of the fields not entered")

        if manager_menu_event == sg.WIN_CLOSED or manager_menu_event == "Exit":
            manager_menu_window.close()
            break
