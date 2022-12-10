
import PySimpleGUI as sg
from Student import Student

with open('Students_data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x:x.split(":"), student_list))
    student_list = list(map(lambda x:Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}



def ActivateRegisterLayout():
    """The register window layout elements properties are here, when func is called open a new window"""
    register_layout = [[sg.Text("Register :")],
        [sg.Text("ID :",size = (10,1)), sg.InputText('',size=(20,1), key='input_ID')],
        [sg.Text("Password :",size = (10,1)), sg.InputText('',size=(20,1), key='input_password', password_char='●')],
        [sg.Text("Name :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text("Secret Word :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_secret_word')],
        [sg.Text(size=(30, 1), key="Error")],
        [sg.Submit(button_text="Register"),
        sg.Exit(pad= ((90, 0), (0,0)))]]

    register_window = sg.Window("Register", register_layout, element_justification='c')
    while True:
        # if the user didn't fill one of the fields the bool will be false and register won't close
        Register_success = False
        register_event, register_values = register_window.read()
        if register_event == "Register":
            input_ID = register_values['input_ID']
            input_password = register_values['input_password']
            input_name = register_values['input_name']
            input_secret_word = register_values['input_secret_word']
            if input_ID == '' or input_password == '' or input_name == '' or input_secret_word == '':
                register_window["Error"].update("One or more of the fields not entered")
            else:
                with open('Students_data.txt', 'a') as file:
                    file.write(input_ID + ':' + input_password + ':' + input_name + ':' + input_secret_word + "\n")
                    file.close()
                student_dict.update({input_ID: Student(input_ID, input_password, input_name, input_secret_word)})
                Register_success = True

        if register_event == sg.WIN_CLOSED or register_event == "Exit" or (register_event == "Register" and Register_success):
            register_window.close()
            break
        """TO DO :
        - check if ID already registered
        """
