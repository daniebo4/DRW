import PySimpleGUI as sg
from Student import Student
import time

with open('data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x:x.split(":"), student_list))
    student_list = list(map(lambda x:Student(x[0],x[1],x[2],x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}

def CheckLogin(ID,Password):
    """a function that checks if ID and password are matching"""
    if ID in student_dict.keys():
        return student_dict[ID].password == Password
    return False

def GetForgotPassword(Username,ID,Secret):
    """function that returns current password """
    if ID in student_dict:
        if student_dict[ID].username == Username and student_dict[ID].secret_word == Secret:
            return student_dict[ID].password
        else :
            return "ID exists but username or secret word do not"
    else:
        return "ID doesn't exists"

def Register():
    """The register window layout elements properties are here, when func is called open a new window"""
    register_layout = [[sg.Text("Register :")],
        [sg.Text("ID :",size = (10,1)), sg.InputText('',size=(20,1), key='input_ID')],
        [sg.Text("Password :",size = (10,1)), sg.InputText('',size=(20,1), key='input_password', password_char='●')],
        [sg.Text("Name :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text("Secret Word :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_secret_word')],
        [sg.Text(size=(30, 1), key="Error")],
        [sg.Submit(button_text="Register"),
        sg.Exit(pad= ((90, 0), (0,0)))]]

    register_window = sg.Window("Register", register_layout)
    while True:
        Register_success = False #if the user didnt fill one of the fields the bool will be false and register wont close
        register_event, register_values = register_window.read()
        if register_event == "Register":
            input_ID = register_values['input_ID']
            input_password = register_values['input_password']
            input_name = register_values['input_name']
            input_secret_word = register_values['input_secret_word']
            if input_ID == '' or input_password == '' or input_name == '' or input_secret_word == '':
                register_window["Error"].update("One or more of the fields not entered")
            else:
                with open('data.txt', 'a') as file:
                    file.write(input_ID + ':' + input_password + ':' + input_name + ':' + input_secret_word + "\n")
                    file.close()
                student_dict.update({input_ID : Student(input_ID, input_password, input_name, input_secret_word)})
                Register_success = True

        if register_event == sg.WIN_CLOSED or register_event == "Exit" or (register_event == "Register" and Register_success):
            register_window.close()
            break
        """TO DO :
        - check if ID already registered
        """

def ChangePassword():
    change_password_layout = [[sg.Text("Change Password")],
                              [sg.Text("ID :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Current Password :", size=(15, 1)),
                               sg.InputText('', size=(20, 1), key='input_current_password', password_char='●')],
                              [sg.Text("New Password :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_new_password', password_char='●')],
                              [sg.Text("Repeat Password :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_repeat_new_password', password_char='●')],
                              [sg.Text(size=(30, 1), key="Error")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((190, 0), (0, 0)))]]

    change_password_window = sg.Window("Change Password", change_password_layout)
    while True:
        Change_success = False
        change_password_event, change_password_values = change_password_window.read()
        if change_password_event == "Confirm":
            input_ID = change_password_values['input_ID']
            input_current_password = change_password_values['input_current_password']
            input_new_password = change_password_values['input_new_password']
            input_repeat_new_password = change_password_values['input_repeat_new_password']

            if input_ID == '' or input_current_password == '' or input_new_password == '' or input_repeat_new_password == '' :
                change_password_window["Error"].update("One or more of the fields not entered")
            else:
                if input_ID in student_dict.keys():
                    if student_dict[input_ID].password == input_current_password:
                        if input_new_password == input_repeat_new_password:
                            student_dict[input_ID].password = input_new_password
                            Change_success = True
                            with open('data.txt', 'a') as file:
                                # find how to write to the correct line in file
                                file.write(input_ID + ':' + input_password + ':' + input_name + ':' + input_secret_word + "\n")
                                file.close()
                        else:
                            change_password_window["Error"].update("New passwords dont match")
                    else:
                        change_password_window["Error"].update("Current password not correct")
                else:
                    change_password_window["Error"].update("ID doesnt exist")

        if change_password_event == sg.WIN_CLOSED or change_password_event == "Exit" or Change_success:
            change_password_window.close()
            break

def ForgotPassword():
    forgot_password_layout = [[sg.Text("Forgot Password")],
                              [sg.Text("Username :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_username')],
                              [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Secret Word :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_secret_word')],
                              [sg.Text(size=(30, 1), key="Output")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((150, 0), (0, 0)))]]

    forgot_password_window = sg.Window("Forgot Password", forgot_password_layout)
    while True:
        forgot_password_event, forgot_password_values = forgot_password_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            if input_username == '' or input_ID == '' or input_secret_word == '':
                forgot_password_window["Output"].update("One or more of the fields not entered")
            else:
                if GetForgotPassword(input_username,input_ID,input_secret_word) not in ("ID exists but username or secret word do not","ID doesn't exists"):
                    forgot_password_window["Output"].update(GetForgotPassword(input_username,input_ID,input_secret_word))


        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            forgot_password_window.close()
            break

def StudentMenu():
    StudentMenu_layout = [[sg.Text("Forgot Password")],
                              [sg.Text("Username :", size=(10, 1)),
                               sg.InputText('', size=(20, 1), key='input_username')],
                              [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Secret Word :", size=(10, 1)),
                               sg.InputText('', size=(20, 1), key='input_secret_word')],
                              [sg.Text(size=(30, 1), key="Error")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((150, 0), (0, 0)))]]

    StudentMenu_window = sg.Window("Forgot Password", StudentMenu_layout)
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

login_layout = [[sg.Text("Welcome to the design department\ninventory management system !")],
          [sg.Text("ID :",size = (10,1)), sg.InputText('',size=(20,1), key='input_ID'), sg.Submit(button_text="Change password")],
          [sg.Text("Password :",size = (10,1)), sg.InputText('',size=(20,1), key='input_password', password_char='●'),sg.Submit(button_text=" Forgot password ")],
          [sg.Text(size=(30, 1), key="Error")],
          [sg.Submit(button_text="Log in"),
           sg.Submit(button_text="Register"),
           sg.Exit(pad= ((210, 0), (0,0)))]]

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
            if CheckLogin(input_ID,input_password):
                StudentMenu()
            else:
                login_window["Error"].update("ID or password incorrect")

    if login_event == "Register":
        Register()

    if login_event == "Change password":
        ChangePassword()

    if login_event == " Forgot password ": # There are spaces before and after the string
        ForgotPassword()

    if login_event == "Exit" or login_event == sg.WIN_CLOSED:
        #time.sleep(5)
        break

login_window.close()

