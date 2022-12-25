import PySimpleGUI as sg

import PySimpleGUI as sg
from database_Personas import DataBase
import main
import os


# remove current manager parameter to rating functions ?
# make rating not possible after manager already rated item
def rate(rating, item_name):
    """func to rate an item and update it in the database"""
    for item in main.db.item_dict.values():
        if item_name == item.name:
            temp_item_num_raters = float(item.num_raters)  # change the string to float for conculataion
            temp_item_num_raters += 1
            # change the result to str to update the dict data
            item.rating = str(
                round((((float(item.rating) * (temp_item_num_raters - 1)) + rating) / temp_item_num_raters), 2))
            item.num_raters = str(temp_item_num_raters)
    item_file = main.project_root_dir + '\\Items_data.txt'
    item_rating_temp = ""
    with open(item_file, 'w+') as file:  # update the database
        for i in main.db.item_dict.values():
            item_rating_temp = i.rating
            file.write(
                f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                f"{i.num_raters}:{i.owner}:{i.status}\n")
    main.db = DataBase(main.project_root_dir + '\\managers_data.txt',
                       main.project_root_dir + '\\managers_data.txt',
                       main.project_root_dir + '\\Items_data.txt')
    return item_rating_temp


def open_rate_window(current_manager, item_name):
    """func to create rating window and mange it"""
    rate_layout = [[sg.Text("Rate Item")],
                   [sg.Button('1', size=(4, 1)), sg.Button('2', size=(4, 1)), sg.Button('3', size=(4, 1)),
                    sg.Button('4', size=(4, 1)), sg.Button('5', size=(4, 1))],
                   ]

    rate_window = sg.Window("Rate Menu", rate_layout, element_justification='c')
    while True:
        rate_event, rate_values = rate_window.read()

        if isinstance(rate_event, str):  # check all the options of rate (1 to 5)
            rate(int(rate_event), item_name)
            rate_window.close()
            break

        if rate_event == sg.WIN_CLOSED:
            rate_window.close()
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

def request_item(current_manager, item_id):
    """func to request item to loan"""
    if item_id in main.db.item_dict:  # check if the item is exist in the database
        main.db.item_dict[item_id].owner = current_manager.ID
    else:
        return False

    # update the owner of the item in the database
    item_file = main.project_root_dir + '\\Items_data.txt'
    with open(item_file, 'w+') as file:
        for i in main.db.item_dict.values():
            file.write(
                f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:"
                f"{i.rating}:{i.num_raters}:{i.owner}:{i.status}\n")
    main.db = DataBase(main.project_root_dir + '\\managers_data.txt',
                       main.project_root_dir + '\\managers_data.txt',
                       main.project_root_dir + '\\Items_data.txt')
    return True


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
    """func to create and manage the menu of the persona user type manager"""
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getAvailableItemTable()
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
                open_rate_window(current_manager, item_name)
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

