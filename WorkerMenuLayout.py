import PySimpleGUI as sg
from Student import Student

with open('data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x: x.split(":"), student_list))
    student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}


def ActivateWorkerMenu():
    WorkerMenu_layout = [[sg.Text("Worker Menu")],
                         [sg.Text("Username :", size=(10, 1)),
                          sg.InputText('', size=(20, 1), key='input_username')],
                         [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                         [sg.Text("Secret Word :", size=(10, 1)),
                          sg.InputText('', size=(20, 1), key='input_secret_word')],
                         [sg.Text(size=(30, 1), key="Error")],
                         [sg.Submit(button_text="Confirm"),
                          sg.Exit(pad=((150, 0), (0, 0)))]]

    StudentMenu_window = sg.Window("Forgot Password", WorkerMenu_layout)
    while True:
        forgot_password_event, forgot_password_values = StudentMenu_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                StudentMenu_window["Error"].update("One or more of the fields not entered")

        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            StudentMenu_window.close()
            break
