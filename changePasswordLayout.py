import PySimpleGUI as sg
from database_Personas import Student
from database_Personas import Data_base
import main

def open_change_password_window():
    change_password_layout = [[sg.Text("Change Password")],
                              [sg.Text("ID :", size=(15, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                              [sg.Text("Current Password :", size=(15, 1)),
                               sg.InputText('', size=(20, 1), key='input_current_password', password_char='●')],
                              [sg.Text("New Password :", size=(15, 1)),
                               sg.InputText('', size=(20, 1), key='input_new_password', password_char='●')],
                              [sg.Text("Repeat Password :", size=(15, 1)),
                               sg.InputText('', size=(20, 1), key='input_repeat_new_password', password_char='●')],
                              [sg.Text(size=(30, 1), key="Error")],
                              [sg.Submit(button_text="Confirm"),
                               sg.Exit(pad=((190, 0), (0, 0)))]] #fdsg

    change_password_window = sg.Window("Change Password", change_password_layout)
    while True:
        change_success = False
        change_password_event, change_password_values = change_password_window.read()
        if change_password_event == "Confirm":
            input_ID = change_password_values['input_ID']
            input_current_password = change_password_values['input_current_password']
            input_new_password = change_password_values['input_new_password']
            input_repeat_new_password = change_password_values['input_repeat_new_password']

            if input_ID == '' or input_current_password == '' or input_new_password == '' or input_repeat_new_password == '':
                change_password_window["Error"].update("One or more of the fields not entered")
            else:
                if input_ID not in main.db.student_dict:
                    change_password_window["Error"].update("ID doesnt exist")
                elif main.db.student_dict[input_ID].password != input_current_password:
                    change_password_window["Error"].update("Current password not correct")
                elif input_new_password != input_repeat_new_password:
                    change_password_window["Error"].update("New passwords don't match")
                else:
                    main.db.student_dict[input_ID].password = input_new_password
                    change_success = True
                    with open('Students_data.txt', 'w') as file:
                        # find how to write to the correct line in file
                        for s in main.db.student_dict.values():
                            file.write(f"{s.ID}:{s.password}:{s.name}:{s.secret_word}\n")

        if change_password_event == sg.WIN_CLOSED or change_password_event == "Exit" or change_success:
            change_password_window.close()
            break
