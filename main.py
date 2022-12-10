import PySimpleGUI as sg
from Database_Personas import Student
from Database_Personas import Worker
import StudentMenuLayout
import ChangePasswordLayout
import RegisterLayout
import ForgotPasswordLayout
import WorkerMenuLayout

import time

with open('Students_data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x: x.split(":"), student_list))
    student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}

with open('Workers_data.txt', 'r') as file:
    Worker_list = file.readlines()
    Worker_list = list(map(lambda x: x.split(":"), Worker_list))
    Worker_list = list(map(lambda x: Worker(x[0], x[1], x[2], x[3]), Worker_list))
    Worker_dict = {s.ID: s for s in Worker_list}


def CheckLoginStudent(ID, Password):
    """a function that checks if ID and password are matching"""
    if ID in student_dict.keys():
        return student_dict[ID].password == Password
    return False


def CheckLoginWorker(ID, Password):
    if ID in Worker_dict.keys():
        return Worker_dict[ID].password == Password
    return False


login_layout = [[sg.Text("Welcome to the design department\ninventory management system !")],
                [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID'),
                 sg.Submit(button_text="Change password")],
                [sg.Text("Password :", size=(10, 1)),
                 sg.InputText('', size=(20, 1), key='input_password', password_char='●'),
                 sg.Submit(button_text=" Forgot password ")],
                [sg.Text(size=(30, 1), key="Error")],
                [sg.Submit(button_text="Log in"),
                 sg.Submit(button_text="Register"),
                 sg.Exit(pad=((210, 0), (0, 0)))]]

login_window = sg.Window("Inventory Management System ", login_layout)

# Main event loop
while True:
    login_event, login_values = login_window.read()

    if login_event == "Log in":
        input_ID = login_values['input_ID']
        input_password = login_values['input_password']

        if input_ID == '' and input_password == '':
            login_window["Error"].update("ID and password not entered")

        elif input_password == '':
            login_window["Error"].update("Password not entered")

        elif input_ID == '':
            login_window["Error"].update("ID not entered")

        else:

            # checks first if the user is a student
            if CheckLoginStudent(input_ID, input_password):
                StudentMenuLayout.ActivateStudentMenu()

            # else checks if the user is a worker and matching password
            elif CheckLoginWorker(input_ID, input_password):
                WorkerMenuLayout.ActivateWorkerMenu()

            else:
                login_window["Error"].update("ID or password incorrect")

    if login_event == "Register":
        RegisterLayout.ActivateRegisterLayout()

    if login_event == "Change password":
        ChangePasswordLayout.ActivateChangePasswordMenu()

    if login_event == " Forgot password ":  # There are spaces before and after the string
        ForgotPasswordLayout.ActivatForgotPassword()

    if login_event == "Exit" or login_event == sg.WIN_CLOSED:
        break

login_window.close()
