import PySimpleGUI as sg
from database_Personas import Student
import main


def open_student_window():
    student_menu_layout = [[sg.Text("Student Menu")],
                           [sg.Text("Secret Word :", size=(10, 1)),
                           sg.InputText('', size=(20, 1), key='input_secret_word')],
                           [sg.Text(size=(30, 1), key="Error")],
                           [sg.Submit(button_text="Confirm"),
                           sg.Exit(pad=((150, 0), (0, 0)))]]

    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c')
    while True:
        forgot_password_event, forgot_password_values = student_menu_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                student_menu_window["Error"].update("One or more of the fields not entered")

        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            student_menu_window.close()
            break
