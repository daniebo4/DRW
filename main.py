import PySimpleGUI as sg
from Layouts import forgotPasswordLayout, changePasswordLayout, workerMenuLayout, studentMenuLayout, registerLayout, \
    managerMenuLayout
from DataBase import db

sg.set_options(font=("Arial Baltic", 16))

sg.change_look_and_feel('systemdefaultforreal')


def mainMenu():
    # Main Menu Window Layout:
    frame = [[sg.Image('logo.png')],
             [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID', do_not_clear=False),
              sg.Submit(button_text="Change password")],
             [sg.Text("Password :", size=(10, 1)),
              sg.InputText('', size=(20, 1), key='input_password', password_char='●', do_not_clear=False),
              sg.Submit(button_text=" Forgot password ")],
             [sg.Text(size=(30, 1), key="Error")],
             [sg.Submit(button_text="Log in", button_color=('Green on Lightgrey')),
              sg.Submit(button_text="Register"),
              sg.Exit(pad=((330, 0), (0, 0)), button_color=('Brown on Lightgrey'), size=(7, 1))]]
    login_layout = [[sg.Frame("", frame)]]

    login_window = sg.Window("Inventory Management System ", login_layout, element_justification='c', finalize=True
                             ,icon='favicon.ico', use_ttk_buttons=True, border_depth=10,
                             titlebar_background_color='Lightgrey', ttk_theme='clam'
                             , auto_size_buttons=True)
    login_window.BorderDepth = 50
    login_window['input_ID'].bind("<Return>", "_Enter")
    login_window['input_password'].bind("<Return>", "_Enter")
    # Window Layout Conditions,according to button clicked by user:
    while True:
        login_event, login_values = login_window.read()

        if login_event == "Log in" or login_event == "input_ID" + "_Enter" or login_event == "input_password" + "_Enter":
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
                    db.addToStudentBacklog(input_ID)


                # else checks if the user is a worker
                elif db.check_login_worker(input_ID, input_password) and input_ID != 'admin':
                    workerMenuLayout.open_worker_window(db.worker_dict[input_ID])
                    db.addToWorkerBacklog(input_ID)

                elif db.check_login_worker(input_ID, input_password):
                    managerMenuLayout.open_manager_window()

                # conclude that user is not registered / details incorrect
                else:
                    login_window["Error"].update("ID or password incorrect")

        if login_event == "Register":
            registerLayout.open_register_window()

        if login_event == "Change password":
            result = changePasswordLayout.open_change_password_window()
            if result is True:
                login_window["Error"].update("Password changed successfully !")

        if login_event == " Forgot password ":  # There are spaces before and after the string !!!!
            forgotPasswordLayout.open_forgot_password_window()

        if login_event == "Exit" or login_event == sg.WIN_CLOSED:
            break

    login_window.close()


if __name__ == "__main__":
    mainMenu()
