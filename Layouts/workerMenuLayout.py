import PySimpleGUI as sg
from DataBase import db
from Personas import Item
import operator

sg.change_look_and_feel('SystemDefaultForReal')


def sort_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.pop_error('Error in sorting error', 'Exception', e)
    return table_data


def confirm_request_item(user_selection, worker_requested_items):
    """This is a function that updates the data of an item owner to be the student's ID """
    if len(user_selection) > 0:  # check if the user choose items to return
        item_id = []
        for index, item in enumerate(worker_requested_items):
            if index in user_selection:
                item_id.append(item[0])

        for ID in item_id:
            db.item_dict[ID].status = 'loan accepted'  # update the status of the returned items in the database
        db.updateItems()
        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_requests_window(current_worker):
    """This is a window that opens when a manager wants to handle the requests
    of items that student requested"""
    # make function work with multiple items
    requested_items_headings = ['ID ', 'Name ', 'Description', 'Rating ', 'Status', "Student's ID", "Student's Name"]
    worker_requested_items = db.get_loan_requested_items()
    frame = [
        [sg.Table(values=worker_requested_items,
                  headings=requested_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True,enable_click_events=True )],
        [sg.Button('Accept', size=(15, 1), button_color=('Green on Lightgrey')),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((240, 0), (0, 0)), size=(7, 1), button_color=('Brown on Lightgrey'))]
    ]
    loan_items_layout = [[sg.Frame("", frame)]]
    requested_items_window = sg.Window("Requested Items", loan_items_layout, finalize=True,
                                       use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                       border_depth=10, titlebar_background_color='Lightgrey', ttk_theme='clam',
                                       )

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
        if isinstance(requested_items_event, tuple):
            # Sorts table based on even clicked
            if requested_items_event[0] == '-TABLE-':
                if requested_items_event[2][0] == -1:
                    col_num_clicked = requested_items_event[2][1]
                    new_table_data = sort_table(worker_requested_items, col_num_clicked)
                    requested_items_window['-TABLE-'].update(new_table_data)
        if requested_items_event == "Exit" or requested_items_event == sg.WIN_CLOSED:
            requested_items_window.close()
            break
    return True


# add conditions!!!
def add_item_check(input_name, input_quantity, input_description):
    """func to approve that all the new item fields are correct"""
    return True


def open_add_window(current_worker):
    """This window is the way that a worker can add a new item to a list with entering its Name/Description """
    frame = [
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
    add_items_layout = [[sg.Frame("", frame)]]
    add_items_window = sg.Window("Add Items", add_items_layout, element_justification='c', size=(200, 300),
                                 use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                 border_depth=10, titlebar_background_color='Lightgrey', ttk_theme='clam')
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


def open_edit_window(current_worker):
    """This window gives access to a worker to edit an items Name/Quantity/Description """
    frame = [
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
         sg.Button('Exit', size=(10, 1), button_color=('Brown on Lightgrey')),
         sg.Exit(pad=((50, 0), (50, 0)), button_color=('Brown on Lightgrey'))]]
    edit_items_layout = [[sg.Frame("", frame)]]
    edit_items_layout_window = sg.Window("Edit Items", edit_items_layout, element_justification='c', size=(200, 350),
                                         use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                         border_depth=10, titlebar_background_color='Lightgrey', ttk_theme='clam')
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
            db.item_dict[ID].status = 'available'  # update the status of the returned items in the database
            db.item_dict[ID].owner = '0'  # remove previous owner of the returned item
        db.updateItems()

        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_returns_window(current_worker):
    """A window to show the worker what items have been requested to return by all the students"""
    loan_items_headings = ['ID ', 'Name ', 'Loan Date', 'Due Date', 'Description', 'Rating ', 'status']
    worker_loaned_items = db.get_return_requested_items()
    frame = [
        [sg.Table(values=worker_loaned_items,
                  headings=loan_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True,enable_click_events=True )],
        [sg.Button('Accept', size=(15, 1), button_color=('Green on Lightgrey')),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((135, 0), (0, 0)), size=(7, 1), button_color=('Brown on Lightgrey'))]
    ]
    loan_items_layout = [[sg.Frame("", frame)]]

    loan_items_window = sg.Window("Returned Items", loan_items_layout, use_custom_titlebar=False,
                                  icon='favicon.ico', use_ttk_buttons=True, border_depth=10,
                                  titlebar_background_color='Lightgrey', ttk_theme='clam')
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
        if isinstance(loan_items_event, tuple):
            # Sorts table based on even clicked
            if loan_items_event[0] == '-TABLE-':
                if loan_items_event[2][0] == -1:
                    col_num_clicked = loan_items_event[2][1]
                    new_table_data = sort_table(worker_loaned_items, col_num_clicked)
                    loan_items_window['-TABLE-'].update(new_table_data)
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
    current_inventory_headings = ['Item', 'Quantity', 'Loan Period (weeks)', 'Rating ', 'Description']
    current_inventory = db.getAvailableItemTable_forMenu()
    frame = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=80,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True,
                  enable_click_events=True)],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Requests', size=(15, 1)),
         sg.Button('Returns', size=(15, 1)),
         sg.Exit(pad=((315, 0), (0, 0)), size=(7, 1), button_color=('Brown on Lightgrey'))]
    ]
    worker_menu_layout = [[sg.Frame("", frame)]]

    worker_menu_window = sg.Window("Worker Menu", worker_menu_layout, element_justification='c',
                                   use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                   border_depth=10, titlebar_background_color='Lightgrey', ttk_theme='clam')
    while True:
        worker_menu_event, worker_menu_values = worker_menu_window.read()
        worker_menu_window["Error"].update("")

        if worker_menu_event == "Requests":
            open_requests_window(current_worker)

        if isinstance(worker_menu_event, tuple):
            # Sorts table based on even clicked
            if worker_menu_event[0] == '-TABLE-':
                if worker_menu_event[2][0] == -1:
                    col_num_clicked = worker_menu_event[2][1]
                    new_table_data = sort_table(current_inventory, col_num_clicked)
                    worker_menu_window['-TABLE-'].update(new_table_data)

        if worker_menu_event == "Returns":
            open_returns_window(current_worker)
            worker_menu_window.close()
            open_worker_window(current_worker)

        if worker_menu_event == sg.WIN_CLOSED or worker_menu_event == "Exit":
            worker_menu_window.close()
            break
