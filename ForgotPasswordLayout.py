import PySimpleGUI as sg
from Student import Student

with open('data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x: x.split(":"), student_list))
    student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}


def GetForgotPassword(Username, ID, Secret):
    """function that returns current password """
    if ID in student_dict:
        if student_dict[ID].username == Username and student_dict[ID].secret_word == Secret:
            return student_dict[ID].password
        else:
            return "ID exists but username or secret word do not"
    else:
        return "ID doesn't exists"


def ActivatForgotPassword():
    forgot_password_layout = [[sg.Text("Forgot Password",justification='center')],
                              [sg.Text("Username :", size=(10, 1)),
                               sg.InputText('', size=(20, 1), key='input_username')],
                              [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Secret Word :", size=(10, 1)),
                               sg.InputText('', size=(20, 1), key='input_secret_word')],
                              [sg.Text(size=(30, 1), key="Output")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((150, 0), (0, 0)))],]

    forgot_password_window = sg.Window("Forgot Password", forgot_password_layout, resizable=True, finalize=True, element_justification='c')
    while True:
        forgot_password_event, forgot_password_values = forgot_password_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                forgot_password_window["Output"].update("One or more of the fields not entered")
            else:
                if GetForgotPassword(input_username, input_ID, input_secret_word) not in (
                        "ID exists but username or secret word do not", "ID doesn't exists"):
                    forgot_password_window["Output"].update(
                        GetForgotPassword(input_username, input_ID, input_secret_word))

        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            forgot_password_window.close()
            break
