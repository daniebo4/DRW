import PySimpleGUI as sg
from DataBase import db

errors = ("One or more fields not provided",
          "ID can only contain numbers",
          "ID exists but name or secret word doesn't",
          "ID doesn't exist or password incorrect")

sg.change_look_and_feel('systemdefaultforreal')


def get_forgot_password(Name, ID, Secret):
    """function that returns current password"""
    if Name == '' or ID == '' or Secret == '':
        return errors[0]
    if not ID.isdigit() and Name != 'admin':
        return errors[1]
    if ID in db.student_dict:
        if db.student_dict[ID].name == Name and db.student_dict[ID].secret_word == Secret:
            return db.student_dict[ID].password
        else:
            return errors[2]
    elif ID in db.worker_dict:
        if ID in db.worker_dict[ID].name == Name and db.worker_dict[ID].secret_word == Secret:
            return db.worker_dict[ID].password
        else:
            return errors[2]
    else:
        return errors[3]


def open_forgot_password_window():
    """build forgot password window"""
    frame = [[sg.Text("Forgot Password", justification='center')],
             [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
             [sg.Text("Name :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_name')],
             [sg.Text("Secret Word :", size=(10, 1)),
              sg.InputText('', size=(20, 1), key='input_secret_word')],
             [sg.Text(size=(30, 1), key="Output")],
             [sg.Submit(button_text="Confirm", button_color=('Green on Lightgrey')),
              sg.Exit(pad=((205, 0), (0, 0)), button_color=('Brown on Lightgrey'), size=(7, 1))]]
    forgot_password_layout = [[sg.Frame("", frame)]]

    forgot_password_window = sg.Window("Forgot Password", forgot_password_layout, resizable=True,
                                       element_justification='c', finalize=True
                                       , icon='favicon.ico', use_ttk_buttons=True, border_depth=10,
                                       titlebar_background_color='Lightgrey', ttk_theme='clam'
                                       , auto_size_buttons=True)
    while True:
        forgot_password_event, forgot_password_values = forgot_password_window.read()
        if forgot_password_event == "Confirm":
            input_name = forgot_password_values['input_name']
            input_ID = forgot_password_values['input_ID']
            input_secret_word = forgot_password_values['input_secret_word']

            forgot_password_window["Output"].update(get_forgot_password(input_name, input_ID, input_secret_word))

        if forgot_password_event == sg.WIN_CLOSED or forgot_password_event == "Exit":
            forgot_password_window.close()
            break
