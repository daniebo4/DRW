import PySimpleGUI as sg
from database_Personas import Student

with open('Students_data.txt', 'r') as file:
    student_list = file.readlines()
    student_list = list(map(lambda x: x.split(":"), student_list))
    student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
    student_dict = {s.ID: s for s in student_list}


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
                               sg.Exit(pad=((190, 0), (0, 0)))]]

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
                if input_ID not in student_dict:
                    change_password_window["Error"].update("ID doesnt exist")
                elif student_dict[input_ID].password != input_current_password:
                    change_password_window["Error"].update("Current password not correct")
                elif input_new_password != input_repeat_new_password:
                    change_password_window["Error"].update("New passwords don't match")
                else:
                    student_dict[input_ID].password = input_new_password
                    change_success = True
                    with open('data.txt', 'a') as file:
                        pass
                        # find how to write to the correct line in file

        if change_password_event == sg.WIN_CLOSED or change_password_event == "Exit" or change_success:
            change_password_window.close()
            break
