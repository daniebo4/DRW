import datetime
import PySimpleGUI as sg
from DataBase import db
from DataBase import DataBase
import operator

sg.change_look_and_feel('SystemDefaultForReal')


def sort_available_items_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    isNum = False

    if col_num_clicked == 2:  # if chosen column is load period , convert all fields to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = int(item[col_num_clicked])

    elif col_num_clicked == 3:  # if chosen column is rating , convert all fields to type float for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = float(item[col_num_clicked])

    table_data = None
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error('Error in sorting error', 'Exception', e)

    if table_data == data:
        table_data = list(reversed(table_data))

    if isNum:
        for item in table_data:
            item[col_num_clicked] = str(item[col_num_clicked])

    return table_data


def sort_my_items_table(data, col_num_clicked):
    """tries to sort the data given to it based on what operator has been clicked in table"""
    isNum, isDate = False, False
    min_date = datetime.date(datetime.MINYEAR, 1, 1)

    if col_num_clicked == 0:  # if chosen column is ID , convert all fields to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = int(item[col_num_clicked])

    elif col_num_clicked in (3, 4):  # if chosen column is rating , convert all fields to type float for correct sort
        isDate = True
        for item in data:
            if item[col_num_clicked] == '':
                item[col_num_clicked] = min_date

    if col_num_clicked == 5:  # if chosen column is ID , convert all fields to type int for correct sort
        isNum = True
        for item in data:
            item[col_num_clicked] = float(item[col_num_clicked])

    table_data = None
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error('Error in sorting error', 'Exception', e)

    if table_data == data:
        table_data = list(reversed(table_data))

    if isNum:
        for item in table_data:
            item[col_num_clicked] = str(item[col_num_clicked])

    elif isDate:
        for item in data:
            if item[col_num_clicked] == min_date:
                item[col_num_clicked] = ''

    return table_data


def rate(rating, item_name):
    """func to rate an item and update it in the database"""
    if not isinstance(rating, int):
        return 'The rating is not an integer'
    for item in db.item_dict.values():
        if item_name == item.name:
            if item.rating == '':
                item.rating = 0
            temp_item_num_raters = float(item.num_raters)  # change the string to float for calculation
            temp_item_num_raters += 1  # change the result to str to update the dict data
            item.rating = str(
                round((((float(item.rating) * (temp_item_num_raters - 1)) + rating) / temp_item_num_raters), 2))
            item.num_raters = str(temp_item_num_raters)
    db.updateItems()
    return 'Update rating successful'


def open_rate_window(item_name):
    """func to create rating window and mange it"""
    frame = [[sg.Text(f"Rate Item : {item_name}")],
             [sg.Button('1', size=(4, 1)), sg.Button('2', size=(4, 1)), sg.Button('3', size=(4, 1)),
              sg.Button('4', size=(4, 1)), sg.Button('5', size=(4, 1))],
             ]
    rate_layout = [[sg.Frame("", frame)]]

    rate_window = sg.Window("Rate Menu", rate_layout, element_justification='c', use_custom_titlebar=False,
                            icon='favicon.ico', use_ttk_buttons=True, border_depth=10,
                            titlebar_background_color='Lightgrey', ttk_theme='clam')
    while True:
        rate_event, rate_values = rate_window.read()

        if isinstance(rate_event, str):  # check all the options of rate (1 to 5)
            rate(int(rate_event), item_name)
            rate_window.close()
            break

        if rate_event == sg.WIN_CLOSED:
            rate_window.close()
            break


def return_item(user_selection, student_loaned_items):
    if len(user_selection) > 0:  # check if the user chose items to return
        item_id = []
        for index, item in enumerate(student_loaned_items):
            if index in user_selection:
                item_id.append(item[0])

        item_rated_set = set()
        for ID in item_id:
            if db.item_dict[ID].status == 'loan requested':
                db.item_dict[ID].status = 'available'
                db.item_dict[ID].owner = ''
                db.item_dict[ID].aq_date = ''
                db.item_dict[ID].du_date = ''
            else:
                db.item_dict[ID].status = 'return requested'  # update the status of the returned items in the database
                if db.item_dict[ID].name not in item_rated_set:
                    open_rate_window(db.item_dict[ID].name)
                    item_rated_set.add(db.item_dict[ID].name)
        db.updateItems()
        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_my_items_window(current_student):
    """func to create and manage loaned item window"""
    my_items_headings = ['ID ', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating ', 'Status']
    student_loaned_items = db.get_students_loaned_items(current_student)
    frame = [
        [sg.Table(values=student_loaned_items,
                  headings=my_items_headings,
                  col_widths=[5, 15, 10, 10, 20, 10, 10],
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True,
                  enable_click_events=True)],
        [sg.Button('Return', size=(7, 1)),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((600, 0), (0, 0)), button_color='Brown on Lightgrey')]
    ]
    my_items_layout = [[sg.Frame("", frame)]]

    my_items_window = sg.Window("My Items", my_items_layout, use_custom_titlebar=False, icon='favicon.ico',
                                use_ttk_buttons=True, border_depth=10, titlebar_background_color='Lightgrey',
                                ttk_theme='clam')
    while True:
        my_items_event, my_items_values = my_items_window.read()
        if my_items_event == 'Return':  # check if student want to return items
            user_selection = my_items_values['-TABLE-']
            output = return_item(user_selection, student_loaned_items)
            if output:  # refresh to the window to show changes
                my_items_window.close()
                open_my_items_window(current_student)
            else:  # warning if the user not choose item to return
                my_items_window["Error"].update("No Items Selected !")
        if isinstance(my_items_event, tuple):
            # Sorts table based on even clicked
            if my_items_event[0] == '-TABLE-':
                if my_items_event[2][0] == -1:
                    col_num_clicked = my_items_event[2][1]
                    student_loaned_items = sort_my_items_table(student_loaned_items, col_num_clicked)
                    my_items_window['-TABLE-'].update(student_loaned_items)
        if my_items_event == "Exit" or my_items_event == sg.WIN_CLOSED:
            my_items_window.close()
            break


# to do : make function work with multiple items
def request_item(current_student, item_id):
    """Goes through item database and tries to find an item that has been requested if it did
    return true and updates the item"""
    if item_id in db.item_dict:  # check if the item exists in the database
        # if yes then change the status in data to loan requested
        db.item_dict[item_id].owner = current_student.ID
        db.item_dict[item_id].status = 'loan requested'
        db.item_dict[item_id].aq_date = datetime.date.today()
        db.item_dict[item_id].du_date = db.item_dict[item_id].aq_date \
                                        + datetime.timedelta(weeks=int(db.item_dict[item_id].loan_period))
        db.updateItems()
        return True

    return False


def open_request_item_window(current_student, item_id):
    """create and manage request to loan item window"""
    frame = [
        [sg.Text("Are you sure you want to loan ?")],
        [sg.Text(f"The {db.item_dict[item_id].name} wil be due to return by "
                 f"{datetime.date.today() + datetime.timedelta(weeks=int(db.item_dict[item_id].loan_period))}")],
        [sg.Button('Yes', button_color=('green on Lightgrey')),
         sg.Button('No', button_color=('brown on Lightgrey'))]

    ]
    request_item_layout = [[sg.Frame("", frame)]]
    request_item_window = sg.Window("Request Item", request_item_layout, element_justification='c',
                                    use_custom_titlebar=False,
                                    icon='favicon.ico', use_ttk_buttons=True, border_depth=10,
                                    titlebar_background_color='Lightgrey', ttk_theme='clam')

    while True:
        # check if the user is sure if he wants to loan the item was chosen
        request_item_event, request_item_values = request_item_window.read()
        if request_item_event == "Yes":
            request_item(current_student, item_id)
            request_item_window.close()
            break
        if request_item_event == "No" or request_item_event == sg.WIN_CLOSED:
            request_item_window.close()
            break
    request_item_window.close()


def open_student_window(current_student):
    """func to create and manage the menu of the persona user type student"""
    current_inventory_headings = ['Item', 'Quantity', 'Loan Period (weeks)', 'Rating ', 'Description']
    current_inventory = db.getAvailableItemTable_forMenu()
    frame = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  col_widths=[14, 8, 9, 8, 24],
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True, enable_click_events=True)],
        [sg.Text(size=(30, 1), key="Error")],
        [sg.Button('Request Item', size=(15, 1)),
         sg.Button('My Items', size=(25, 1)),
         sg.Exit(pad=((135, 0), (0, 0)), size=(7, 1), button_color=('Brown on Lightgrey'))]
    ]
    student_menu_layout = [[sg.Frame("", frame)]]
    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c', finalize=True,
                                    use_custom_titlebar=False, icon='favicon.ico', use_ttk_buttons=True,
                                    border_depth=20, titlebar_background_color='Lightgrey', ttk_theme='clam')
    while True:
        student_menu_event, student_menu_values = student_menu_window.read()
        student_menu_window["Error"].update("")
        if student_menu_event == "Request Item":
            if student_menu_values['-TABLE-']:
                if len(student_menu_values['-TABLE-']) == 1:
                    chosen_item_idx = student_menu_values['-TABLE-'][0]
                    chosen_item_name = current_inventory[chosen_item_idx][0]
                    chosen_item_ID = None
                    for item in db.item_dict.values():  # choose specific item to loan from database
                        if item.name == chosen_item_name and item.owner in (None, "", '0'):
                            chosen_item_ID = item.ID
                            break
                    open_request_item_window(current_student, chosen_item_ID)
                    student_menu_window.close()
                    open_student_window(current_student)
                else:
                    student_menu_window["Error"].update("Can't request multiple items at once")
            else:  # error to user if he didn't choose item
                student_menu_window["Error"].update("No Items selected")

        if student_menu_event == "My Items":
            open_my_items_window(current_student)
            student_menu_window.close()
            open_student_window(current_student)

        if isinstance(student_menu_event, tuple):
            # Sorts table based on even clicked
            if student_menu_event[0] == '-TABLE-':
                if student_menu_event[2][0] == -1:
                    col_num_clicked = student_menu_event[2][1]
                    current_inventory = sort_available_items_table(current_inventory, col_num_clicked)
                    student_menu_window['-TABLE-'].update(current_inventory)
        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
