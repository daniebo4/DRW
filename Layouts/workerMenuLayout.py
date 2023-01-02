import PySimpleGUI as sg
import datetime

from Layouts.studentMenuLayout import open_my_items_window
from database_Personas import DataBase
import main
import os


def confirm_request_item(user_selection, worker_requested_items):
    """This is a function that updates the data of an item owner to be the student's ID """
    if len(user_selection) > 0:  # check if the user choose items to return
        item_id = []
        for index, item in enumerate(worker_requested_items):
            if index in user_selection:
                item_id.append(item[0])

        for ID in item_id:
            main.db.item_dict[ID].status = 'loan accepted'  # update the status of the returned items in the database

        item_file = main.project_root_dir + '\\Items_data.txt'
        with open(item_file, 'w') as file:
            for i in main.db.item_dict.values():
                """
                for every item in items dict writes to a text file all of its keys this way we can track
                our items in the system
                """
                file.write(
                    f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                    f"{i.num_raters}:{i.owner}:{i.status}:{i.loan_period}\n")

        main.db = DataBase(main.project_root_dir + '\\workers_data.txt',
                           main.project_root_dir + '\\Workers_data.txt',
                           main.project_root_dir + '\\Items_data.txt')
        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_requests_window(current_worker):
    """This is a window that opens when a manager wants to handle the requests
    of items that student requested"""
    # make function work with multiple items
    requested_items_headings = ['ID', 'Name', 'Description', 'Rating', 'Status', "Student's ID", "Student's Name"]
    worker_requested_items = main.db.get_loan_requested_items()
    loan_items_layout = [
        [sg.Table(values=worker_requested_items,
                  headings=requested_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, )],
        [sg.Button('Accept', size=(15, 1)),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((125, 0), (0, 0)))]
    ]

    requested_items_window = sg.Window("Requested Items", loan_items_layout)
    while True:
        requested_items_event, requested_items_values = requested_items_window.read()
        if requested_items_event == 'Accept':
            user_selection = requested_items_values['-TABLE-']
            output = confirm_request_item(user_selection, worker_requested_items)
            if output:  # refresh to the window to show changes
                requested_items_window.close()
                open_requests_window(current_worker)
            else:  # warning if the user not choose item to return
                requested_items_window["Error"].update("No Items Selected !")
        if requested_items_event == "Exit" or requested_items_event == sg.WIN_CLOSED:
            requested_items_window.close()
            break

    # update the owner of the item in the database
    item_file = main.project_root_dir + '\\Items_data.txt'
    with open(item_file, 'w+') as file:
        for i in main.db.item_dict.values():
            file.write(
                f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:"
                f"{i.rating}:{i.num_raters}:{i.owner}:{i.status}:{i.loan_period}\n")
    main.db = DataBase(main.project_root_dir + '\\workers_data.txt',
                       main.project_root_dir + '\\Workers_data.txt',
                       main.project_root_dir + '\\Items_data.txt')
    return True


# add conditions
def add_item_check(input_name, input_quantity, input_description):
    return True


def open_add_window(current_worker):
    """This window is the way that a worker can add a new item to a list with entering its Name/Description """
    add_items_layout = [
        [sg.Text('Item Name')],
        [sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text('Item Quantity')],
        [sg.InputText('', size=(20, 1), key='input_quantity')],
        [sg.Text('Item Description')],
        [sg.InputText('', size=(20, 1), key='input_description')],
        [sg.Text('Loan period (months)')],
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
                if len(main.db.item_dict.keys()) == 0:
                    input_ID = 1
                else:
                    input_ID = max([int(ID) for ID in main.db.item_dict.keys()]) + 1  # gets maximum Id in item list

                with open('Items_data.txt', 'a') as file:
                    file.write(f"{input_ID}:{input_name}:{datetime.date.today()}::"
                               f"{input_description}::{0}::available:{input_loan_time_period}\n")
                input_quantity -= 1
                while input_quantity > 0:
                    input_ID += 1
                    with open('Items_data.txt', 'a') as file:
                        file.write(f"{input_ID}:{input_name}:{datetime.date.today()}::"
                                   f"{input_description}::::available:{input_loan_time_period}\n")
                    input_quantity -= 1
                main.db = DataBase(main.project_root_dir + '\\Students_data.txt',
                                   main.project_root_dir + '\\Workers_data.txt',
                                   main.project_root_dir + '\\Items_data.txt')
            else:
                add_items_window["Error"].update("One or more of the fields are invalid")

        if add_items_event == sg.WIN_CLOSED or add_items_event == "Exit" or (
                add_items_event == "Add" and add_item_check_res):
            add_items_window.close()
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


def confirm_return_item(user_selection, worker_loaned_items):
    """This is a function that removes the data of an item owner to be available"""
    if len(user_selection) > 0:  # check if the user choose items to return
        item_id = []
        for index, item in enumerate(worker_loaned_items):
            if index in user_selection:
                item_id.append(item[0])

        for ID in item_id:
            main.db.item_dict[ID].status = 'available'  # update the status of the returned items in the database
            main.db.item_dict[ID].owner = '0'  # remove previous owner of the returned item

        item_file = main.project_root_dir + '\\Items_data.txt'
        with open(item_file, 'w') as file:
            for i in main.db.item_dict.values():
                file.write(
                    f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                    f"{i.num_raters}:{i.owner}:{i.status}:{i.loan_period}\n")

        main.db = DataBase(main.project_root_dir + '\\workers_data.txt',
                           main.project_root_dir + '\\Workers_data.txt',
                           main.project_root_dir + '\\Items_data.txt')
        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_returns_window(current_worker):
    """A window to show the worker what items have been requested to return by all the students"""
    loan_items_headings = ['ID', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating', 'status']
    worker_loaned_items = main.db.get_return_requested_items()
    loan_items_layout = [
        [sg.Table(values=worker_loaned_items,
                  headings=loan_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, )],
        [sg.Button('Accept', size=(15, 1)),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((300, 0), (0, 0)))]
    ]

    loan_items_window = sg.Window("Returned Items", loan_items_layout)
    while True:
        loan_items_event, loan_items_values = loan_items_window.read()
        if loan_items_event == 'Accept':  # check if worker want to accept the request return items
            user_selection = loan_items_values['-TABLE-']
            output = confirm_return_item(user_selection, worker_loaned_items)
            if output:  # refresh to the window to show changes
                loan_items_window.close()
                open_returns_window(current_worker)
            else:  # warning if the user not choose item to return
                loan_items_window["Error"].update("No Items Selected !")
        if loan_items_event == "Exit" or loan_items_event == sg.WIN_CLOSED:
            loan_items_window.close()
            break


def open_worker_window(current_worker):
    """
    This is the main window of the worker where he can choose what action to perform :
    Add - adds an item to the system by calling open_add_window
    Remove - choose to remove an item from the system by calling
    Edit - edits an item from the system by calling
    requests - opens a window to manage all the request mad by students for items
    returns - opens a window to manage the returns of all students
    """
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Arrival Date', 'Loan Period (months)', 'Description',
                                  'Rating']
    current_inventory = main.db.getAvailableItemTable_forMenu()
    worker_menu_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True)],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Add', size=(15, 1)),
         sg.Button('Remove', size=(15, 1)),
         sg.Button('Edit', size=(15, 1)),
         sg.Button('Requests', size=(15, 1)),
         sg.Button('Returns', size=(15, 1)),
         sg.Exit(pad=((0, 0), (0, 0)))]
    ]

    worker_menu_window = sg.Window("worker Menu", worker_menu_layout, element_justification='c')
    while True:
        worker_menu_event, worker_menu_values = worker_menu_window.read()
        worker_menu_window["Error"].update("")

        if worker_menu_event == "Requests":
            open_requests_window(current_worker)

        if worker_menu_event == "Add":
            open_add_window(current_worker)
            worker_menu_window.close()
            open_worker_window(current_worker)

        if worker_menu_event == "Edit":
            open_edit_window(current_worker)

        if worker_menu_event == "Returns":
            open_returns_window(current_worker)
            worker_menu_window.close()
            open_worker_window(current_worker)

        if worker_menu_event == sg.WIN_CLOSED or worker_menu_event == "Exit":
            worker_menu_window.close()
            break
