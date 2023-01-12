import datetime
import PySimpleGUI as sg
from DataBase import db

sg.change_look_and_feel('systemdefaultforreal')


# to do : make rating not possible after student already rated item
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
    frame = [[sg.Text("Rate Item")],
                   [sg.Button('1', size=(4, 1)), sg.Button('2', size=(4, 1)), sg.Button('3', size=(4, 1)),
                    sg.Button('4', size=(4, 1)), sg.Button('5', size=(4, 1))],
                   ]
    rate_layout = [[sg.Frame("", frame)]]

    rate_window = sg.Window("Rate Menu", rate_layout, element_justification='c', use_custom_titlebar=True,
                            titlebar_icon='icon.png', use_ttk_buttons=True, border_depth=10,
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

        for ID in item_id:
            if db.item_dict[ID].status == 'loan requested':
                db.item_dict[ID].status = 'available'
                db.item_dict[ID].owner = ''
                db.item_dict[ID].aq_date = ''
                db.item_dict[ID].du_date = ''
            else:
                db.item_dict[ID].status = 'return requested'  # update the status of the returned items in the database
        db.updateItems()
        return True
    else:  # write error to the user if he didn't choose items to return
        return False


def open_my_items_window(current_student):
    """func to create and manage loaned item window"""
    my_items_headings = ['ID ', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating ', 'status']
    student_loaned_items = db.get_students_loaned_items(current_student)
    frame = [
        [sg.Table(values=student_loaned_items,
                  headings=my_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  enable_events=True, )],
        [sg.Button('Return', size=(7, 1)),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((550, 0), (0, 0)),button_color=('Brown on Lightgrey'))]
    ]
    my_items_layout = [[sg.Frame("", frame)]]

    my_items_window = sg.Window("My Items", my_items_layout, use_custom_titlebar=True, titlebar_icon='icon.png',
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
        [sg.Button('Yes',button_color=('green on Lightgrey')),
         sg.Button('No',button_color=('brown on Lightgrey'))]

    ]
    request_item_layout = [[sg.Frame("", frame)]]
    request_item_window = sg.Window("Request Item", request_item_layout, element_justification='c',
                                    use_custom_titlebar=True,
                                    titlebar_icon='icon.png', use_ttk_buttons=True, border_depth=10,
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
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True, )],
        [sg.Text(size=(15, 1), key="Error")],
        [sg.Button('Request Item', size=(15, 1)),
         sg.Button('My Items', size=(15, 1)),
         sg.Button('Rate', size=(15, 1)),
         sg.Exit(pad=((93, 0), (0, 0)),button_color=('Brown on Lightgrey'))]
    ]
    student_menu_layout = [[sg.Frame("", frame)]]
    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c', finalize=True,
                                    use_custom_titlebar=True, titlebar_icon='icon.png', use_ttk_buttons=True,
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

        if student_menu_event == "Rate":
            # check if the user choose item before pressing on rate button
            if len(student_menu_values['-TABLE-']) == 1:
                chosen_item_idx = student_menu_values['-TABLE-'][0]
                chosen_item_name = current_inventory[chosen_item_idx][0]
                open_rate_window(chosen_item_name)
                student_menu_window.close()
                open_student_window(current_student)
                # warning to the user if he chose more than one item to rate in the same time
            elif len(student_menu_values['-TABLE-']) > 1:
                student_menu_window["Error"].update("You can only rate one item at a time")
            else:  # warning to the user if he isn't choose item before pressing on rate button
                student_menu_window["Error"].update("choose item to rate!")

        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
