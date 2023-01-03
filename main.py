import PySimpleGUI as sg
from Layouts import forgotPasswordLayout, changePasswordLayout, workerMenuLayout, studentMenuLayout, registerLayout, \
    managerMenuLayout
from DataBase import db
import datetime


def mainMenu():
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
                if db.check_login_student(input_ID, input_password):
                    studentMenuLayout.open_student_window(db.student_dict[input_ID])
                    item_file = db.file_dir_student_backlog

                    with open(item_file, 'a') as file:
                        file.write(
                            f"{db.student_dict[input_ID].ID}:{db.student_dict[input_ID].name}:{datetime.date.today()}\n")

                # else checks if the user is a worker
                elif db.check_login_worker(input_ID, input_password) and input_ID != 'admin':
                    workerMenuLayout.open_worker_window(db.worker_dict[input_ID])
                    item_file = db.file_dir_worker_backlog
                    with open(item_file, 'a') as file:
                        file.write(
                            f"{db.worker_dict[input_ID].ID}:{db.worker_dict[input_ID].name}:{datetime.date.today()}\n")

                elif db.check_login_worker(input_ID, input_password):
                    managerMenuLayout.open_manager_window(db.worker_dict[input_ID])

                # conclude that user is not registered / details incorrect
                else:
                    login_window["Error"].update("ID or password incorrect")

        if login_event == "Register":
            registerLayout.open_register_window()

        if login_event == "Change password":
            changePasswordLayout.open_change_password_window()

        if login_event == " Forgot password ":  # There are spaces before and after the string !!!!
            forgotPasswordLayout.open_forgot_password_window()

        if login_event == "Exit" or login_event == sg.WIN_CLOSED:
            break

    login_window.close()


if __name__ == "__main__":
    mainMenu()
