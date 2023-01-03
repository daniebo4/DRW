from datetime import datetime
import PySimpleGUI as sg
from DataBase import db
from Personas import Item


def add_item_check(input_name, input_quantity, input_description):
    return True


def open_add_window_manger(current_worker):
    """This window is the way that a worker can add a new item to a list with entering its Name/Description """
    add_items_layout = [
        [sg.Text('Item Name')],
        [sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text('Item Quantity')],
        [sg.InputText('', size=(20, 1), key='input_quantity')],
        [sg.Text('Item Description')],
        [sg.InputText('', size=(20, 1), key='input_description')],
        [sg.Text('Loan period (weeks)')],
        [sg.InputText('', size=(20, 1), key='input_time_period')],
        [sg.Text(size=(10, 0), key="Error")],
        [sg.Button('Add', size=(10, 1)),
         sg.Button('Exit', size=(10, 1))]]
    add_items_window = sg.Window("Add Items", add_items_layout, element_justification='c', size=(200, 300))
    while True:
        add_item_check_res = False
        add_items_event, add_items_values = add_items_window.read()
        if add_items_event == 'Add':
            input_name = add_items_values['input_name']
            input_quantity = int(add_items_values['input_quantity'])
            input_description = add_items_values['input_description']
            input_loan_time_period = add_items_values['input_time_period']
            add_item_check_res = add_item_check(input_name, input_quantity, input_description)
            if add_item_check_res:
                if len(db.item_dict.keys()) == 0:
                    input_ID = 1
                else:
                    input_ID = max([int(ID) for ID in db.item_dict.keys()]) + 1  # gets maximum Id in item list

                while input_quantity > 0:
                    db.addItem(Item(str(input_ID), input_name, "", "", input_description, '0', '0', '0', "available",
                                    input_loan_time_period))
                    input_ID += 1
                    input_quantity -= 1
            else:
                add_items_window["Error"].update("One or more of the fields are invalid")

        if add_items_event == sg.WIN_CLOSED or add_items_event == "Exit" or (
                add_items_event == "Add" and add_item_check_res):
            add_items_window.close()
            break


def open_manage_workers():
    """Managing workers window"""
    manage_workers_headings = ['Name', 'ID']

    with open(db.file_dir_student_backlog, 'r') as file:  # Students database
        """opens the file of the student to read and create a list from"""
        backlog_list = file.readlines()
        backlog_list = list(map(lambda x: x.split(":"), backlog_list))

    manage_workers_values = backlog_list
    manage_workers_layout = [
        [sg.Table(values=manage_workers_values,
                  headings=manage_workers_headings,
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  def_col_width=35,
                  enable_events=True, )],
        [sg.Text(size=(15, 1), key="Error")],
        [sg.Button('Add New Worker', size=(15, 1)),
         sg.Button('Remove Worker', size=(15, 1)),
         sg.Exit(pad=((100, 0), (0, 0)))]
    ]
    manage_workers_window = sg.Window("Manage Workers", manage_workers_layout)
    while True:
        manage_workers_event, my_items_values = manage_workers_window.read()
        if manage_workers_event == "Add New Worker":
            if manage_workers_event == "Add New Worker":  # check if student want to return items
                # user_selection = manage_workers_values['-TABLE-']
                # output = add_worker()
                #  manage_workers_window.close()
                add_new_worker()
            else:  # warning if the user not choose item to return
                manage_workers_window["Error"].update("No Items Selected !")
        if manage_workers_event == "Remove Worker":
            remove_worker()
        elif manage_workers_event == "Exit" or manage_workers_event == sg.WIN_CLOSED:
            manage_workers_window.close()
            break


def add_new_worker():
    add_new_worker_layout = [[sg.Text("Add a New Worker:")],
                             [sg.Text("ID :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_ID')],
                             [sg.Text("Password :", size=(10, 1)),
                              sg.InputText('', size=(20, 1), key='input_password', password_char='●')],
                             [sg.Text("Name :", size=(10, 1)), sg.InputText('', size=(20, 1), key='input_name')],
                             [sg.Text("Secret Word :", size=(10, 1)),
                              sg.InputText('', size=(20, 1), key='input_secret_word')],
                             [sg.Text(size=(30, 1), key="Error")],
                             [sg.Submit(button_text="Add"),
                              sg.Exit(pad=((90, 0), (0, 0)))]]

    add_new_worker_window = sg.Window("Add New Worker", add_new_worker_layout, element_justification='c')

    while True:
        add_new_worker_event, add_new_worker_values = add_new_worker_window.read()
        if add_new_worker_event == sg.WIN_CLOSED or add_new_worker_event == "Exit":
            add_new_worker_window.close()
            break


def remove_worker():
    remove_worker_layout = [
        [sg.Text("Are you super duper sure you want to remove this worker?\nThink twice it's alright :")],
        [sg.Button(button_text="Yes"),
         sg.Button(button_text="No"), ]]
    remove_worker_window = sg.Window("Remove Worker", remove_worker_layout, element_justification='c')
    while True:
        remove_worker_event, remove_worker_values = remove_worker_window.read()
        if remove_worker_event == sg.WIN_CLOSED or remove_worker_event == "Yes" or remove_worker_event == "No":
            remove_worker_window.close()
            break


def open_backlog(input_event_personas='StudentsLog'):
    open_backlog_headings = ['ID', 'Name', 'Login dates:']

    if input_event_personas == "StudentsLog":
        with open(db.file_dir_student_backlog, 'r') as file:  # Students database
            """opens the file of the student to read and create a list from"""
            backlog_list = file.readlines()
            backlog_list = list(map(lambda x: x.split(":"), backlog_list))

    elif input_event_personas == "WorkersLog":
        with open(db.file_dir_worker_backlog, 'r') as file:  # Students database
            """opens the file of the student to read and create a list from"""
            backlog_list = file.readlines()
            backlog_list = list(map(lambda x: x.split(":"), backlog_list))

    open_backlog_values = backlog_list
    open_backlog_layout = [[sg.Table(values=open_backlog_values,
                                     headings=open_backlog_headings,
                                     auto_size_columns=False,
                                     display_row_numbers=False,
                                     justification='c',
                                     num_rows=10,
                                     key='-TABLE-',
                                     row_height=35,
                                     col_widths=[20, 20, 35],
                                     enable_events=True, )],
                           [sg.Button('Students Log', size=(10, 1), key='students_log'),
                            sg.Button('Workers Log', size=(10, 1), key='workers_log'),
                            sg.Exit(pad=((800, 0), (0, 0)))]]
    open_backlog_window = sg.Window("Backlog", open_backlog_layout, element_justification='c', size=(700, 500))

    while True:
        open_backlog_event, open_backlog_values = open_backlog_window.read()
        if open_backlog_event == 'students_log':
            open_backlog_window.close()
            open_backlog('StudentsLog')

        elif open_backlog_event == 'workers_log':
            open_backlog_window.close()
            open_backlog("WorkersLog")

        if open_backlog_event == sg.WIN_CLOSED or open_backlog_event == "Exit":
            open_backlog_window.close()
            break


def open_edit_window(current_worker):
    """This window gives access to a worker to edit an items Name/Quantity/Description """
    edit_items_layout = [
        [sg.Text('Item Name')],
        [sg.InputText('', size=(20, 1), key='<item_name>')],
        [sg.Text('Item Quantity')],
        [sg.InputText('', size=(20, 1), key='<item_quantity>')],
        [sg.Text('Item Description')],
        [sg.InputText('', size=(20, 1), key='<item_Description>>')],
        [sg.Text('Due Date')],
        [sg.InputText('', size=(20, 1), key='<item_Date>>')],
        [sg.Text('Due Acquired')],
        [sg.InputText('', size=(20, 1), key='<item_Acquired>>')],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Confirm', size=(10, 1)),
         sg.Button('Exit', size=(10, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    edit_items_layout_window = sg.Window("Edit Items", edit_items_layout, element_justification='c', size=(200, 350))
    while True:
        add_items_layout_event, edit_items_layout_values = edit_items_layout_window.read()
        if add_items_layout_event == sg.WIN_CLOSED or add_items_layout_event == "Exit":
            break

    edit_items_layout_window.close()


def open_manager_window(current_worker):
    """func to create and manage the menu of the persona user type manager"""
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = db.getAvailableItemTable()
    open_manager_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True)],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Add', size=(15, 1)),
         sg.Button('Remove', size=(15, 1)),
         sg.Button('Edit', size=(15, 1)),
         sg.Button('Manage Workers', size=(15, 1)),
         sg.Button('Backlog', size=(15, 1)),
         sg.Exit(pad=((0, 0), (0, 0)))]
    ]

    manager_window = sg.Window("manager Menu", open_manager_layout, element_justification='c')
    while True:
        open_manager_event, open_manager_values = manager_window.read()
        manager_window["Error"].update("")

        if open_manager_event == "Backlog":
            open_backlog()
        if open_manager_event == "Add":
            open_add_window_manger(current_worker)
            manager_window.close()
            open_manager_window(current_worker)

        if open_manager_event == "Edit":
            open_edit_window(current_worker)

        if open_manager_event == "Manage Workers":
            open_manage_workers()

        if open_manager_event == sg.WIN_CLOSED or open_manager_event == "Exit":
            manager_window.close()
            break

