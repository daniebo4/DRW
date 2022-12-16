import os
import PySimpleGUI as sg
from database_Personas import DataBase
from Layouts import forgotPasswordLayout
from Layouts import changePasswordLayout
from Layouts import workerMenuLayout
from Layouts import studentMenuLayout
from Layouts import managerMenuLayout
from Layouts import registerLayout

project_root_dir = os.path.dirname(os.path.abspath(__file__))  # Finds path to current project folder
db = DataBase(project_root_dir + '\\Students_data.txt',
              project_root_dir + '\\Workers_data.txt',
              project_root_dir + '\\Items_data.txt')  # Gets path to


# student and worker database


def mainMenu():
    global db
    # Main event loop
    login_layout = [[sg.Text("Welcome to the design department\n inventory management system !")],
                    [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID'),
                     sg.Submit(button_text="Change password")],
                    [sg.Text("Password :", size=(10, 1)),
                     sg.InputText('', size=(20, 1), key='input_password', password_char='●'),
                     sg.Submit(button_text=" Forgot password ")],
                    [sg.Text(size=(30, 1), key="Error")],
                    [sg.Submit(button_text="Log in"),
                     sg.Submit(button_text="Register"),
                     sg.Exit(pad=((210, 0), (0, 0)))]]

    login_window = sg.Window("Inventory Management System ", login_layout, element_justification='c')
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
                if check_login_student(input_ID, input_password):
                    studentMenuLayout.open_student_window(db.student_dict[input_ID])

                # else checks if the user is a worker
                elif check_login_worker(input_ID, input_password) and input_ID != 'admin':
                    workerMenuLayout.open_worker_window()

                # else check if the user is the admin
                elif check_login_worker(input_ID, input_password):
                    managerMenuLayout.open_manager_window()

                # conclude that user is not registered / details incorrect
                else:
                    login_window["Error"].update("ID or password incorrect")

        if login_event == "Register":
            registerLayout.open_register_window()
            db = DataBase(project_root_dir + '\\Students_data.txt',
                          project_root_dir + '\\Workers_data.txt',
                          project_root_dir + '\\Items_data.txt')

        if login_event == "Change password":
            changePasswordLayout.open_change_password_window()
            db = DataBase(project_root_dir + '\\Students_data.txt',
                          project_root_dir + '\\Workers_data.txt',
                          project_root_dir + '\\Items_data.txt')

        if login_event == " Forgot password ":  # There are spaces before and after the string !!!!
            forgotPasswordLayout.open_forgot_password_window()

        if login_event == "Exit" or login_event == sg.WIN_CLOSED:
            break

    login_window.close()


'''def append_to_data_base(input_obj):
    global db
    if isinstance(input_obj, Student):
        db.student_dict[input_obj.ID] = input_obj
    elif isinstance(input_obj, Worker):
        db.worker_dict[input_obj.ID] = input_obj'''  # back up function in case database management system is changed


def check_login_student(ID, Password):
    """a function that checks if student`s ID and password are matching"""
    return ID in db.student_dict and db.student_dict[ID].password == Password


def check_login_worker(ID, Password):
    """a function that checks if worker`s ID and password are matching"""
    return ID in db.worker_dict and db.worker_dict[ID].password == Password


if __name__ == "__main__":
    mainMenu()
