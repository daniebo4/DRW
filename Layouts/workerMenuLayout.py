import PySimpleGUI as sg
from DataBase import db
from Personas import Item
import operator
import datetime

sg.change_look_and_feel('SystemDefaultForReal')


def items_status():
    """This window lets the worker watch a list of items whose status is not 'available' ,
        meaning they are currently requested , loaned or return requested
        """
    # Window Layout:
    current_inventory_headings = ['ID ', 'Item', 'Owner ID', 'Owner name', 'Status', 'Loan Date', 'Due Date',
                                  'Loan Period (weeks)', 'Description']
    current_inventory = db.getItemStatuses_forWorker()
    frame = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True, enable_click_events=True)]]
    item_status_layout = [[sg.Frame("", frame)]]

    item_status_window = sg.Window("Item Status", item_status_layout, element_justification='c', icon='favicon.ico',
                                   use_ttk_buttons=True, border_depth=10,
                                   titlebar_background_color='Lightgrey', ttk_theme='clam'
                                   , auto_size_buttons=True)
    while True:
        item_status_event, item_status_values = item_status_window.read()

        if isinstance(item_status_event, tuple):
            # Sorts table based on even clicked
            if item_status_event[0] == '-TABLE-':
                if item_status_event[2][0] == -1 and item_status_event[2][1] != -1:
                    col_num_clicked = item_status_event[2][1]
                    current_inventory = sort_item_status_table(current_inventory, col_num_clicked)
                    item_status_window['-TABLE-'].update(current_inventory)

        if item_status_event == sg.WIN_CLOSED or item_status_event == "Exit":
            item_status_window.close()
            break


def sort_item_status_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    isNum, isDate = False, False
    if col_num_clicked in (
            0, 2, 7):  # if chosen column is ID or loan period , convert all ID to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = int(item[col_num_clicked])

    min_date = datetime.date(datetime.MINYEAR, 1, 1)
    if col_num_clicked in (5, 6):  # if chosen column is date , convert empty fields to minimum date for correct sort
        isDate = True
        for item in data:
            if item[col_num_clicked] == '':
                item[col_num_clicked] = min_date

    table_data = None
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error('Error in sorting error', 'Exception', e)

    if table_data == data:  # detect if table is already sorted , if True , reverse the sort
        table_data = list(reversed(table_data))

    if isNum:
        for item in table_data:
            item[col_num_clicked] = str(item[col_num_clicked])

    elif isDate:
        for item in data:
            if item[col_num_clicked] == min_date:
                item[col_num_clicked] = ''

    return table_data


def sort_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    isNum = False

    if col_num_clicked in (0, 5):  # if chosen column is ID , convert all ID to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = int(item[col_num_clicked])

    if col_num_clicked == 3:  # if chosen column is rating , convert empty fields to float for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = float(item[col_num_clicked])

    table_data = None
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error('Error in sorting error', 'Exception', e)

    if table_data == data:  # detect if table is already sorted , if True , reverse the sort
        table_data = list(reversed(table_data))

    if isNum:
        for item in table_data:
            item[col_num_clicked] = str(item[col_num_clicked])

    return table_data


def sort_available_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    isNum = False

    if col_num_clicked in (1, 2):  # if chosen column is number , convert all ID to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = int(item[col_num_clicked])

    if col_num_clicked == 3:  # if chosen column is rating , convert empty fields to float for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = float(item[col_num_clicked])

    table_data = None
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error('Error in sorting error', 'Exception', e)

    if table_data == data:  # detect if table is already sorted , if True , reverse the sort
        table_data = list(reversed(table_data))

    if isNum:
        for item in table_data:
            item[col_num_clicked] = str(item[col_num_clicked])

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
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, enable_click_events=True, )],
        [sg.Button('Accept', size=(15, 1), button_color=('Green on Lightgrey')),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((240, 0), (0, 0)), size=(7, 1), button_color=('Brown on Lightgrey'))]
    ]
    loan_items_layout = [[sg.Frame("", frame)]]
    requested_items_window = sg.Window("Requested Items", loan_items_layout, finalize=True,
                                       use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                       border_depth=10, titlebar_background_color='Lightgrey',
                                       ttk_theme='clam', element_justification='c')

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
                    worker_requested_items = sort_table(worker_requested_items, col_num_clicked)
                    requested_items_window['-TABLE-'].update(worker_requested_items)
        if requested_items_event == "Exit" or requested_items_event == sg.WIN_CLOSED:
            requested_items_window.close()
            break
    return True


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
            db.item_dict[ID].aq_date = ''
            db.item_dict[ID].du_date = ''
            db.updateItems()

        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_returns_window(current_worker):
    """A window to show the worker what items have been requested to return by all the students"""
    loan_items_headings = ['ID ', 'Name ', 'Description', 'Rating ', 'Status', "Student's ID", "Student's Name"]
    worker_loaned_items = db.get_return_requested_items()
    frame = [
        [sg.Table(values=worker_loaned_items,
                  headings=loan_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, enable_click_events=True)],
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
                    worker_loaned_items = sort_table(worker_loaned_items, col_num_clicked)
                    loan_items_window['-TABLE-'].update(worker_loaned_items)
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
         sg.Button('Item Status', size=(15, 1)),
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
                    current_inventory = sort_available_table(current_inventory, col_num_clicked)
                    worker_menu_window['-TABLE-'].update(current_inventory)

        if worker_menu_event == "Returns":
            open_returns_window(current_worker)
            worker_menu_window.close()
            open_worker_window(current_worker)

        if worker_menu_event == 'Item Status':
            items_status()

        if worker_menu_event == sg.WIN_CLOSED or worker_menu_event == "Exit":
            worker_menu_window.close()
            break
