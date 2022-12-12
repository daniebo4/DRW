import PySimpleGUI as sg


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
        register_success = False  # checks validity of input , if True - window will close
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
                    file.write(f"{input_ID}:{input_password}:{input_name}:{input_secret_word}\n")
                register_success = True

        if register_event == sg.WIN_CLOSED or register_event == "Exit" or (
                register_event == "Register" and register_success):
            register_window.close()
            break
        """TO DO :
        - check if ID already registered
        """
