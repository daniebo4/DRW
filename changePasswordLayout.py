import PySimpleGUI as sg
import main

change_errors= ("One or more of the fields not entered", "ID can only contain numbers", "ID doesnt exist",
               "Current password not correct", "New passwords don't match" )

'''
def change_student(input_ID, input_new_password):
    """writes the student in Student_data"""
    change_success = True
    
'''

def attempt_to_change(input_ID, input_current_password, input_new_password, input_repeat_new_password):
    """The function gets the input and tries to create a new student
    account and returns a string based on what happened """
    if input_ID == '' or input_current_password == '' or input_new_password == '' or input_repeat_new_password == '':
        return change_errors[0]
    if not input_ID.isdigit():
        return change_errors[1]
    else:
        if input_ID not in main.db.student_dict:
            return change_errors[2]
        elif main.db.student_dict[input_ID].password != input_current_password:
            return change_errors[3]
        elif input_new_password != input_repeat_new_password:
            return change_errors[4]
        else:
            main.db.student_dict[input_ID].password = input_new_password
            with open('Students_data.txt', 'w') as file:
                for s in main.db.student_dict.values():
                    file.write(f"{s.ID}:{s.password}:{s.name}:{s.secret_word}\n")
            return True


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

    change_password_window = sg.Window("Change Password", change_password_layout, element_justification='c')
    while True:
        change_success = False
        change_password_event, change_password_values = change_password_window.read()
        if change_password_event == "Confirm":
            input_ID = change_password_values['input_ID']
            input_current_password = change_password_values['input_current_password']
            input_new_password = change_password_values['input_new_password']
            input_repeat_new_password = change_password_values['input_repeat_new_password']
            # The system calls the function below to try to register with the input it got from the GUI
            change_check_res = attempt_to_change(input_ID, input_current_password, input_new_password, input_repeat_new_password)
            if change_check_res is not True:
                change_password_window["Error"].update(change_check_res)

        if change_password_event == sg.WIN_CLOSED or change_password_event == "Exit" or change_check_res is True:
            change_password_window.close()
            break
