import PySimpleGUI as sg
from database_Personas import Worker
from database_Personas import Data_base
import main


def open_worker_window():
    worker_menu_layout = [[sg.Text("Manager Menu")],
                          [sg.Text("Username :", size=(10, 1)),
                          sg.InputText('', size=(20, 1), key='input_username')],
                          [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                          [sg.Text("Secret Word :", size=(10, 1)),
                          sg.InputText('', size=(20, 1), key='input_secret_word')],
                          [sg.Text(size=(30, 1), key="Error")],
                          [sg.Submit(button_text="Confirm"),
                          sg.Exit(pad=((150, 0), (0, 0)))]]

    worker_menu_window = sg.Window("Forgot Password", worker_menu_layout, element_justification='c')
    while True:
        forgot_password_event, forgot_password_values = worker_menu_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                worker_menu_window["Error"].update("One or more of the fields not entered")

        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            worker_menu_window.close()
            break
