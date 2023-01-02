from datetime import datetime

import PySimpleGUI as sg

import PySimpleGUI as sg
from database_Personas import DataBase
import main
import os

def add_item_check(input_name, input_quantity, input_description):
    return True

def open_add_window(current_worker):
    #This window is the way that a worker can add a new item to a list with entering its Name/Description
    add_items_layout = [
        [sg.Text('Item Name')],
        [sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text('Item Quantity')],
        [sg.InputText('', size=(20, 1), key='input_quantity')],
        [sg.Text('Item Description')],
        [sg.InputText('', size=(20, 1), key='input_description')],
        [sg.Text(size=(10, 0), key="Error")],
        [sg.Button('Add', size=(20, 1)),
         sg.Button('Exit', size=(20, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    add_items_window = sg.Window("Add Items", add_items_layout, element_justification='c', size=(400, 300))
    while True:
        add_item_check_res = False
        add_items_event, add_items_values = add_items_window.read()
        if add_items_event == 'Add':
            input_name = add_items_values['input_name']
            input_quantity = int(add_items_values['input_quantity'])
            input_description = add_items_values['input_description']
            add_item_check_res = add_item_check(input_name, input_quantity, input_description)
            if add_item_check_res:
                input_ID = max([int(ID) for ID in main.db.item_dict.keys()]) + 1  # gets maximum Id in item list
                with open('Items_data.txt', 'a') as file:
                    file.write(f"{input_ID}:{input_name}:{datetime.date.today()}::"
                               f"{input_description}::::available\n")
                input_quantity -= 1
                while input_quantity > 0:
                    input_ID += 1
                    with open('Items_data.txt', 'a') as file:
                        file.write(f"{input_ID}:{input_name}:::"
                                   f"{input_description}::::available\n")
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

"""
# manager method ?
def open_manage_workers(current_worker):
    
   #A window to manage the workers with the following funcs:
    #Add New Worker - can add new workers with the permissions
    #Remove worker - can remove a worker

    my_items_headings = ['Name', 'ID']
    worker_loaned_items = main.db.get_workers_loaned_items(current_worker)
    manage_workers_layout = [
        [sg.Table(values=worker_loaned_items,
                  headings=my_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, )],
        [sg.Text(size=(15, 1), key="Error")],
        [sg.Button('Add New Worker', size=(15, 1)),
         sg.Button('Remove Worker', size=(15, 1)),
         sg.Button('Return', size=(15, 1)),
         sg.Exit(pad=((300, 0), (0, 0)))]
    ]
    
    my_items_window = sg.Window("My Items", my_items_layout)
    while True:
        my_items_event, my_items_values = my_items_window.read()
        if my_items_event == 'Return':  # check if worker want to return items
            user_selection = my_items_values['-TABLE-']
            output = return_item(user_selection, worker_loaned_items)
            if output:  # refresh to the window to show changes
                my_items_window.close()
                open_my_items_window(current_worker)
            else:  # warning if the user not choose item to return
                my_items_window["Error"].update("No Items Selected !")
        if my_items_event == "Exit" or my_items_event == sg.WIN_CLOSED:
            my_items_window.close()
            break

"""
"""
def return_item(user_selection, manager_loaned_items):
    if len(user_selection) > 0:  # check if the user choose items to return
        item_id = []
        for index, item in enumerate(manager_loaned_items):
            if index in user_selection:
                item_id.append(item[0])

        for ID in item_id:
            main.db.item_dict[ID].status = 'pending'  # update the status of the returned items in the database

        item_file = main.project_root_dir + '\\Items_data.txt'
        with open(item_file, 'w') as file:
            for i in main.db.item_dict.values():
                file.write(
                    f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                    f"{i.num_raters}:{i.owner}:{i.status}\n")

        main.db = DataBase(main.project_root_dir + '\\managers_data.txt',
                           main.project_root_dir + '\\managers_data.txt',
                           main.project_root_dir + '\\Items_data.txt')
        return True
    else:  # write error to the user if he didn't choose items to return
        return False
"""
def open_manage_workers():
    """Managing workers window"""
    manage_workers_headings = ['Name', 'ID']
    manage_workers_values = [['Daniel', '42069'], ['Shlomo', '00000001']]
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
         sg.Exit(pad=((550, 0), (0, 0)))]
    ]
    manage_workers_window = sg.Window("Manage Workers", manage_workers_layout)
    while True:
        manage_workers_event, my_items_values = manage_workers_window.read()
        if manage_workers_event == "Add New Worker":
            if manage_workers_event == "Add New Worker":  # check if student want to return items
                #user_selection = manage_workers_values['-TABLE-']
                #output = add_worker()
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
    remove_worker_layout = [[sg.Text("Are you super duper sure you want to remove this worker?\nThink twice it's alright :")],
                            [sg.Button(button_text="Yes"),
                            sg.Button(button_text="No"),]]
    remove_worker_window = sg.Window("Remove Worker", remove_worker_layout, element_justification='c')
    while True:
        remove_worker_event, remove_worker_values = remove_worker_window.read()
        if remove_worker_event == sg.WIN_CLOSED or remove_worker_event == "Yes" or remove_worker_event == "No":
            remove_worker_window.close()
            break
def open_backlog():
    open_backlog_headings = ['Name', 'ID', 'Logins:']
    open_backlog_values = [['Daniel', '42069','420'], ['Shlomo', '00000001','-5']]
    open_backlog_layout =   [[sg.Table(values=open_backlog_values,
                              headings=open_backlog_headings,
                              auto_size_columns=False,
                              display_row_numbers=False,
                              justification='c',
                              num_rows=10,
                              key='-TABLE-',
                              row_height=35,
                              col_widths=[20,20,35],
                              enable_events=True, )],
                              [sg.Exit(pad=((800, 0), (0, 0)))]]
    open_backlog_window = sg.Window("Backlog", open_backlog_layout, element_justification='c')

    while True:
        open_backlog_event, open_backlog_values = open_backlog_window.read()
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

"""
def open_request_item_window(current_manager, item_id):
    #create and manage request to loan item window
    # make function work with multiple items
    request_item_layout = [
        [sg.Text("Are you sure you want to loan ?")],
        [sg.Button('Yes', ),
         sg.Button('No', )]
        # add return date please
    ]

    request_item_window = sg.Window("Request Item", request_item_layout)

    while True:
        # check if the user is sure if he want to lan the item that he was choose
        request_item_event, request_item_values = request_item_window.read()
        if request_item_event == "Yes":
            request_item(current_manager, item_id)
            request_item_window.close()
            break
        if request_item_event == "No" or request_item_event == sg.WIN_CLOSED:
            request_item_window.close()
            break
    request_item_window.close()
"""

def open_manager_window(current_worker):
    """func to create and manage the menu of the persona user type manager"""
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getAvailableItemTable()
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

    open_manager_window = sg.Window("manager Menu", open_manager_layout, element_justification='c')
    while True:
        open_manager_event, open_manager_values = open_manager_window.read()
        open_manager_window["Error"].update("")

        if open_manager_event == "Backlog":
            open_backlog()
        if open_manager_event == "Add":
            open_add_window(current_worker)
            open_manager_window.close()
        if open_manager_event == "Edit":
            open_edit_window(current_worker)
        """
        if add_new_worker_event == "Request Item":
            if add_new_worker_values['-TABLE-']:
                # insert if condition multiple item selection
                if len(add_new_worker_values['-TABLE-']) == 1:
                    item_idx = add_new_worker_values['-TABLE-'][0]
                    item_id = current_inventory[item_idx][0]
                    open_request_item_window(current_manager, item_id)
                add_new_worker_window.close()
                open_manager_window(current_manager)
            else:  # warning to the user if he isn't choose item
                add_new_worker_window["Error"].update("No Items selected")
"""
        if open_manager_event == "Manage Workers":
            open_manage_workers()
        """
        if add_new_worker_event == "Rate":
            # check if the user choose item before pressing on rate button
            if len(add_new_worker_values['-TABLE-']) == 1:
                item_idx = add_new_worker_values['-TABLE-'][0]
                item_name = current_inventory[item_idx][1]
                add_new_worker_window.close()
                open_manager_window(current_manager)
                # warning to the user if he chose more than one item to rate in the same time
            elif len(add_new_worker_values['-TABLE-']) > 1:
                add_new_worker_window["Error"].update("You can only rate one item at a time")
            else: # warning to the user if he isn't choose item before pressing on rate button
                add_new_worker_window["Error"].update("choose item to rate!")
"""
        if open_manager_event == sg.WIN_CLOSED or open_manager_event == "Exit":
            open_manager_window.close()
            break

