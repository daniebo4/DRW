import PySimpleGUI as sg

import PySimpleGUI as sg
import main
import os

def add_item_check(input_name, input_quantity, input_description):

    return True

def open_add_window(current_worker):
    """ Using this functionality the manager can add items to the system,with the following info:Name,Quantity,Description"""
    # Window Layout:
    add_items_layout = [
        [sg.Text('Item Name')],
        [sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text('Item Quantity')],
        [sg.InputText('', size=(20, 1), key='input_quantity')],
        [sg.Text('Item Description')],
        [sg.InputText('', size=(20, 1), key='input_description')],
        [sg.Text(size=(10, 0), key="Error")],
        [sg.Button('Add', size=(10, 1)),
         sg.Button('Exit', size=(10, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    add_items_window = sg.Window("Add Items", add_items_layout, element_justification='c', size=(200, 250))
    # different actions to perform according to what button user click on
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

# manager method ?
def open_manage_workers(current_worker):
    """
    Using this functionality a manager can view a list of all the workers,add or remove them
    """
    my_items_headings = ['Name', 'ID']
    worker_loaned_items = main.db.get_workers_loaned_items(current_worker)
    # Window Layout:
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
    # different actions to perform according to what button user click on
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


def open_manage_workers():
    """Managing workers window"""
    manage_workers_headings = ['Name', 'ID']
    workers_values = ['Daniel', '42069']
    my_items_layout = [
        [sg.Table(values=workers_values,
                  headings=manage_workers_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
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


def open_request_item_window(current_manager, item_id):
    """create and manage request to loan item window"""
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


def open_manager_window(current_manager):
    """Manager's window in the system,features:
    Viewing all items in storage
    Adding & removing and editing items
    Viewing workers data, adding and removing their users from thes system
    Viewing a log of the system's events
    """
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getAvailableItemTable()
    # Window Layout:
    manager_menu_layout = [
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

    manager_menu_window = sg.Window("manager Menu", manager_menu_layout, element_justification='c')
    # different actions to perform according to what button user click on
    while True:
        manager_menu_event, manager_menu_values = manager_menu_window.read()
        manager_menu_window["Error"].update("")

        if manager_menu_event == "Request Item":
            if manager_menu_values['-TABLE-']:
                # insert if condition multiple item selection
                if len(manager_menu_values['-TABLE-']) == 1:
                    item_idx = manager_menu_values['-TABLE-'][0]
                    item_id = current_inventory[item_idx][0]
                    open_request_item_window(current_manager, item_id)
                manager_menu_window.close()
                open_manager_window(current_manager)
            else:  # warning to the user if he isn't choose item
                manager_menu_window["Error"].update("No Items selected")

        if manager_menu_event == "Manage Workers":
            open_manage_workers()

        if manager_menu_event == "Rate":
            # check if the user choose item before pressing on rate button
            if len(manager_menu_values['-TABLE-']) == 1:
                item_idx = manager_menu_values['-TABLE-'][0]
                item_name = current_inventory[item_idx][1]
                manager_menu_window.close()
                open_manager_window(current_manager)
                # warning to the user if he chose more than one item to rate in the same time
            elif len(manager_menu_values['-TABLE-']) > 1:
                manager_menu_window["Error"].update("You can only rate one item at a time")
            else: # warning to the user if he isn't choose item before pressing on rate button
                manager_menu_window["Error"].update("choose item to rate!")

        if manager_menu_event == sg.WIN_CLOSED or manager_menu_event == "Exit":
            manager_menu_window.close()
            break

