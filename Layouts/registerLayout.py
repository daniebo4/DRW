import PySimpleGUI as sg
import DataBase
from database_Personas import Student
from importlib import reload

register_errors = ("One or more fields not provided", "ID can only contain numbers",
                   "Name can't contain numbers", "ID already exists in system")


def check_register(input_ID, input_password, input_name, input_secret_word):
    if input_ID == '' or input_password == '' or input_name == '' or input_secret_word == '':
        return register_errors[0]
    elif not input_ID.isdigit():
        return register_errors[1]
    elif any(char.isdigit() for char in input_name):
        return register_errors[2]
    elif input_ID in DataBase.db.student_dict:
        return register_errors[3]
    else:
        return True


def open_register_window():
    """The register window layout elements properties are here, when func is called open a new window"""
    register_layout = [[sg.Text("Register :")],
                       [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                       [sg.Text("Password :", size=(10, 1)),
                        sg.InputText('', size=(20, 1), key='input_password', password_char='●')],
                       [sg.Text("Name :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_name')],
                       [sg.Text("Secret Word :", size=(10, 1)),
                        sg.InputText('', size=(20, 1), key='input_secret_word')],
                       [sg.Text(size=(30, 1), key="Error")],
                       [sg.Submit(button_text="Register"),
                        sg.Exit(pad=((90, 0), (0, 0)))]]

    register_window = sg.Window("Register", register_layout, element_justification='c')

    while True:
        register_check_res = False
        register_event, register_values = register_window.read()
        if register_event == "Register":
            input_ID = register_values['input_ID']
            input_password = register_values['input_password']
            input_name = register_values['input_name']
            input_secret_word = register_values['input_secret_word']
            register_check_res = check_register(input_ID, input_password, input_name, input_secret_word)
            if register_check_res is True:
                DataBase.db.addStudent(Student(input_ID, input_password, input_name, input_secret_word))
            else:
                register_window["Error"].update(register_check_res)

        if register_event == sg.WIN_CLOSED or register_event == "Exit" or (
                register_event == "Register" and register_check_res is True):
            register_window.close()
            break
