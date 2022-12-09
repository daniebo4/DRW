import PySimpleGUI as sg

def CheckLogin(Username,Password):
    """a function that returns true or false if the username and password exsists int database"""
    with open(r'data.txt', 'r') as file:
        # read all content from a file using read()
        content = file.read()
        # check if string present or not
        if Username in content and Password in content: return True
    return False


def CheckForgotPassword(Username,ID,Secret):
    """a function that returns true or false if the username and password and secret word are true """
    with open(r'data.txt', 'r') as file:
        # read all content from a file using read()
        content = file.read()
        # check if string present or not
        if Username in content and ID in content and Secret in content : return

def Register():
    """The register window layout elements properties are here, when func is called open a new window"""
    register_layout = [[sg.Text("Register :")],
        [sg.Text("Username :",size = (10,1)), sg.InputText('',size=(20,1), key='input_username')],
        [sg.Text("Password :",size = (10,1)), sg.InputText('',size=(20,1), key='input_password', password_char='●')],
        [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
        [sg.Text("Secret Word :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_secret_word')],
        [sg.Text(size=(30, 1), key="Error")],
        [sg.Submit(button_text="Register"),
        sg.Exit(pad= ((90, 0), (0,0)))]]

    register_window = sg.Window("Register", register_layout)
    while True:
        Register_success = False#if the user didnt fill one of the fields the bool will be false and register wont close
        register_event, register_values = register_window.read()
        if register_event == "Register":
            input_username = register_values['input_username']
            input_password = register_values['input_password']
            input_ID = register_values['input_ID']
            input_secret_word = register_values['input_secret_word']

            if input_username == '' or input_password == '' or input_ID == ''or input_secret_word == '':
                register_window["Error"].update("One or more of the fields not entered")
            else:
                f = open('data.txt','a')
                f.write(input_username+':'+input_password+':'+input_ID+':'+input_secret_word+':'+'Student'+"\n")
                f.close()
                Register_success=True

        if register_event == sg.WIN_CLOSED or register_event == "Exit" or (register_event == "Register" and Register_success==True) :
            register_window.close()
            break

def ChangePassword():
    change_password_layout = [[sg.Text("Change Password")],
                              [sg.Text("Username :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_username')],
                              [sg.Text("Current Password :", size=(15, 1)),
                               sg.InputText('', size=(20, 1), key='input_password', password_char='●')],
                              [sg.Text("New Password :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_new_password', password_char='●')],
                              [sg.Text("Repeat Password :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_repeat_new_password', password_char='●')],
                              [sg.Text(size=(30, 1), key="Error")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((190, 0), (0, 0)))]]

    change_password_window = sg.Window("Change Password", change_password_layout)
    while True:
        change_password_event, change_password_values = change_password_window.read()
        if change_password_event == "Confirm":
            input_username = change_password_values['input_username']
            input_current_password = change_password_values['input_username']


            if input_username == '' or input_ID == '' or input_secret_word == '':
                change_password_window["Error"].update("One or more of the fields not entered")

        if change_password_event == sg.WIN_CLOSED or change_password_event == "Exit":
            change_password_window.close()
            break

def ForgotPassword():
    forgot_password_layout = [[sg.Text("Forgot Password")],
                              [sg.Text("Username :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_username')],
                              [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Secret Word :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_secret_word')],
                              [sg.Text(size=(30, 1), key="Error")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((150, 0), (0, 0)))]]

    forgot_password_window = sg.Window("Forgot Password", forgot_password_layout)
    while True:
        forgot_password_event, forgot_password_values = forgot_password_window.read()
        if forgot_password_event == "Confirm":
            input_username = forgot_password_values['input_username']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']
            print(CheckForgotPassword(input_username,input_ID,input_secret_word))

            if input_username == '' or input_ID == '' or input_secret_word == '':
                forgot_password_window["Error"].update("One or more of the fields not entered")

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
          [sg.Text("Username :",size = (10,1)), sg.InputText('',size=(20,1), key='input_username'), sg.Submit(button_text="Change password")],
          [sg.Text("Password :",size = (10,1)), sg.InputText('',size=(20,1), key='input_password', password_char='●'),sg.Submit(button_text=" Forgot password ")],
          [sg.Text(size=(30, 1), key="Error")],
          [sg.Submit(button_text="Log in"),
           sg.Submit(button_text="Register"),
           sg.Exit(pad= ((210, 0), (0,0)))]]

# Create the window
login_window = sg.Window("Inventory Management System ", login_layout)

# Create an event loop
while True:
    login_event, login_values = login_window.read()
    # End program if user closes window or
    # presses the Exit button
    if login_event == "Log in":
        input_username = login_values['input_username']
        input_password = login_values['input_password']

        if input_username == '' and input_password == '':
            login_window["Error"].update("Username and password not entered")

        elif input_password == '':
            login_window["Error"].update("Password not entered")

        elif input_username == '':
            login_window["Error"].update("Username not entered")

        else:
            if CheckLogin(input_username,input_password):
                StudentMenu()
            else:
                login_window["Error"].update("Username or password incorrect")

    if login_event == "Register":
        Register()

    if login_event == "Change password":
        ChangePassword()

    if login_event == " Forgot password ": # There are spaces before and after the string
        ForgotPassword()

    if login_event == "Exit" or login_event == sg.WIN_CLOSED:
        break

login_window.close()

