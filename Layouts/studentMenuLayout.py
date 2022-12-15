import PySimpleGUI as sg
from database_Personas import DataBase
import main
import os


def selected_row_event():
    pass


def rate(current_student, rating):
    student_loaned_items = main.db.get_students_loaned_items(current_student)
    print('1')



def open_rate_window(current_student):
    enable_events = True
    open_rate_layout = [[sg.Text("Rate Item")],
                        [sg.Button('1', size=(4, 1)), sg.Button('2', size=(4, 1)), sg.Button('3', size=(4, 1)),
                         sg.Button('4', size=(4, 1)), sg.Button('5', size=(4, 1))],
                        ]

    open_rate_window = sg.Window("Rate Menu", open_rate_layout, element_justification='c')
    while True:
        open_rate_event, open_rate_values = open_rate_window.read()

        if open_rate_event == '5':
            rate(current_student, 5)
            open_rate_window.close()
            break

        if open_rate_event == sg.WIN_CLOSED:
            open_rate_window.close()
            break


def open_my_items_window(current_student):
    my_items_headings = ['ID', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating', 'status']
    student_loaned_items = main.db.get_students_loaned_items(current_student)
    my_items_layout = [
        [sg.Table(values=student_loaned_items,
                  headings=my_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, )],
        [sg.Button('Return', size=(15, 1)),
         sg.Exit(pad=((430, 0), (0, 0)))]
    ]

    my_items_window = sg.Window("My Items", my_items_layout)
    while True:
        my_items_event, my_items_values = my_items_window.read()
        if my_items_event == 'Return':
            item_idx = my_items_values['-TABLE-'][0]
            item_id = student_loaned_items[item_idx][0]
            main.db.item_dict[item_id].status = 'pending'
            item_file = main.project_root_dir + '\\Items_data.txt'
            with open(item_file, 'w') as file:
                for i in main.db.item_dict.values():
                    file.write(
                        f"{i.ID}:{i.name}:{i.description}:{i.rating}:{i.du_date}:{i.aq_date}:{i.owner}:{i.status}\n")

            main.db = DataBase(main.project_root_dir + '\\Students_data.txt',
                               main.project_root_dir + '\\Workers_data.txt',
                               main.project_root_dir + '\\Items_data.txt')
            student_loaned_items = main.db.get_students_loaned_items(current_student)
            my_items_window.close()
            open_my_items_window(current_student)
        # main.db.item_dic[ID].status='pending'
        # call to return item function
        if my_items_event == "Exit" or my_items_event == sg.WIN_CLOSED:
            my_items_window.close()
            break


def open_request_item_window(current_student, item_id):
    enable_event = True
    student_loaned_items = main.db.get_students_loaned_items(current_student)
    request_item_layout = [
        [sg.Text("Are you Sure?")],
        [sg.Button('Yes', ),
         sg.Button('No', )]
        # add return date please
    ]

    request_item_window = sg.Window("Request Item", request_item_layout)

    while True:
        request_item_event, request_item_values = request_item_window.read()
        if request_item_event == "Yes":
            main.db.item_dict[item_id].owner = current_student.ID
            item_file = main.project_root_dir + '\\Items_data.txt'
            with open(item_file, 'w+') as file:
                for i in main.db.item_dict.values():
                    file.write(
                        f"{i.ID}:{i.name}:{i.description}:{i.rating}:{i.du_date}:{i.aq_date}:{i.owner}:{i.status}\n")

            request_item_window.close()
            break
        if request_item_event == "No" or request_item_event == sg.WIN_CLOSED:
            request_item_window.close()
            break
    request_item_window.close()


def open_student_window(current_student):
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getItemTable()
    student_menu_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True)],
        [sg.Button('Request Item', size=(15, 1)),
         sg.Button('My Items', size=(15, 1)),
         sg.Button('Rate', size=(15, 1)),
         sg.Exit(pad=((430, 0), (0, 0)))]
    ]

    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c')
    while True:
        student_menu_event, student_menu_values = student_menu_window.read()

        if student_menu_event == "Request Item":
            item_idx = student_menu_values['-TABLE-'][0]
            item_id = current_inventory[item_idx][0]
            open_request_item_window(current_student, item_id)

        if student_menu_event == "My Items":
            open_my_items_window(current_student)

        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
        if student_menu_event == "Rate":
            open_rate_window(current_student)
