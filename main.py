import PySimpleGUI as sg
from database_Personas import Student
from database_Personas import Worker
import forgotPasswordLayout
import changePasswordLayout
import workerMenuLayout
import studentMenuLayout
import registerLayout

# Databases are text files , following lines translate the data to dictionaries for easier access and manipulation
with open('Students_data.txt', 'r') as file: # Students database
    student_list = file.readlines()
    student_list = list(map(lambda x: x.split(":"), student_list))
    student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}

with open('Workers_data.txt', 'r') as file: # Workers database
    worker_list = file.readlines()
    worker_list = list(map(lambda x: x.split(":"), worker_list))
    worker_list = list(map(lambda x: Worker(x[0], x[1], x[2], x[3]), worker_list))
    worker_dict = {w.ID: w for w in worker_list}

def check_login_student(ID, Password):
    """a function that checks if student`s ID and password are matching"""
    return ID in student_dict and student_dict[ID].password == Password

def check_login_worker(ID, Password):
    """a function that checks if worker`s ID and password are matching"""
    return ID in worker_dict and worker_dict[ID].password == Password

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

def main():
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
                if check_login_student(input_ID, input_password):
                    studentMenuLayout.open_student_window()

                # else checks if the user is a worker
                elif check_login_worker(input_ID, input_password):
                    workerMenuLayout.open_worker_window()

                # if

                else:
                    login_window["Error"].update("ID or password incorrect")

        if login_event == "Register":
            registerLayout.open_register_window()
            # changes to students dict made in registerLayout not seen in main's student dict
            # find way to do this without opening databas in each file

        if login_event == "Change password":
            changePasswordLayout.open_change_password_window()

        if login_event == " Forgot password ":  # There are spaces before and after the string
            forgotPasswordLayout.open_forgot_password_window()

        if login_event == "Exit" or login_event == sg.WIN_CLOSED:
            break

    login_window.close()

if __name__ == "__main__":
    main()
