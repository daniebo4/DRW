import PySimpleGUI as sg
from DataBase import db
from Personas import Item, Worker


# to do : complete this func
def add_item_check(input_name, input_quantity, input_description):
    return True


def open_add_window_manger(current_worker):
    """
    Using this functionality the manager can add items to the system,with the following info:Name,Quantity,
    Description and loan period
    """
    # Window Layout:
    add_items_layout = [
        [sg.Text('Item Name:')],
        [sg.InputText('', size=(20, 1), key='input_name')],
        [sg.Text('Item Quantity:')],
        [sg.InputText('', size=(20, 1), key='input_quantity')],
        [sg.Text('Item Description:')],
        [sg.InputText('', size=(20, 1), key='input_description')],
        [sg.Text('Loan period (Weeks):')],
        [sg.InputText('', size=(20, 1), key='input_time_period')],
        [sg.Text(size=(10, 0), key="Error")],
        [sg.Button('Add', size=(10, 1)),
         sg.Button('Exit', size=(10, 1))]]
    add_items_window = sg.Window("Add Items", add_items_layout, element_justification='c', size=(250, 350))
    # Window Layout Conditions,according to button clicked by user:
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
                    input_ID = max([int(ID) for ID in db.item_dict.keys()]) + 1  # gets maximum ID in item list to
                    # generate new, not used item ID

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


# to do : create method in DataBase.py to get list of workers
def edit_worker(chosen_worker_id):
    """Function for edit a worker's info"""
    # Window Layout:
    edit_worker_layout = [
        [sg.Text('New Password:')],
        [sg.InputText('', size=(20, 1), key='<Password>')],
        [sg.Text('New Secret Word:')],
        [sg.InputText('', size=(20, 1), key='<Secret_Word>')],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Confirm', size=(10, 1)),
         sg.Button('Exit', size=(10, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    edit_worker_window = sg.Window("Edit Worker", edit_worker_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        check_info = False
        edit_worker_event, edit_worker_values = edit_worker_window.read()
        Password = edit_worker_values['<Password>']
        Secret_Word = edit_worker_values['<Secret_Word>']
        if edit_worker_event == 'Confirm':
            if Password != '' and Secret_Word != '':
                db.worker_dict[chosen_worker_id].password = Password
                db.worker_dict[chosen_worker_id].secret_word = Secret_Word
                check_info =True
                db.updateWorkers()
            elif Password != '' and Secret_Word == '':
                db.worker_dict[chosen_worker_id].password = Password
                check_info =True
                db.updateWorkers()
            elif Password == '' and Secret_Word != '':
                db.worker_dict[chosen_worker_id].secret_word = Secret_Word
                check_info =True
                db.updateWorkers()
            else:
                edit_worker_window["Error"].update("No Input Data")
        if edit_worker_event == sg.WIN_CLOSED or (edit_worker_event == "Confirm" and check_info==True) or edit_worker_event == "Exit" :
            edit_worker_window.close()
            break


def open_manage_workers():
    """
    Using this functionality the manager can View a list of all the workers in the system and add or remove workers
    """
    # Window Layout:
    current_workers = db.getWorkers()
    manage_workers_headings = ['Name', 'ID']
    manage_workers_layout = [
        [sg.Table(values=current_workers,
                  headings=manage_workers_headings,
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  def_col_width=25,
                  enable_events=True, )],
        [sg.Text(size=(15, 1), key="Error")],
        [sg.Button('Add New Worker', size=(15, 1)),
         sg.Button('Remove Worker', size=(15, 1)),
         sg.Button('Edit Worker', size=(15, 1)),
         sg.Exit(pad=((280, 0), (0, 0)))]
    ]
    manage_workers_window = sg.Window("Manage Workers", manage_workers_layout)
    # Window Layout Conditions,according to button clicked by user:
    while True:
        manage_workers_event, manage_workers_values = manage_workers_window.read()
        if manage_workers_event == "Add New Worker":
            if manage_workers_event == "Add New Worker":
                add_new_worker()

        if manage_workers_event == "Remove Worker":
            if manage_workers_values['-TABLE-']:
                if len(manage_workers_values['-TABLE-']) == 1:
                    chosen_worker_idx = manage_workers_values['-TABLE-'][0]
                    chosen_worker_id = current_workers[chosen_worker_idx][1]
                    remove_worker(chosen_worker_id)
                    manage_workers_window.close()
                    open_manage_workers()
                else:
                    manage_workers_window["Error"].update("multiple Workers Selected !")
            else:  # warning if the user didn't select worker
                manage_workers_window["Error"].update("No Worker Selected !")

        if manage_workers_event == "Edit Worker":
            if manage_workers_values['-TABLE-']:
                if len(manage_workers_values['-TABLE-']) == 1:
                    chosen_worker_idx = manage_workers_values['-TABLE-'][0]
                    chosen_worker_id = current_workers[chosen_worker_idx][1]
                    edit_worker(chosen_worker_id)
                    manage_workers_window.close()
                    open_manage_workers()
                else:
                    manage_workers_window["Error"].update("multiple Workers Selected !")
            else:  # warning if the user didn't select worker
                manage_workers_window["Error"].update("No Worker Selected !")


        elif manage_workers_event == "Exit" or manage_workers_event == sg.WIN_CLOSED:
            manage_workers_window.close()
            break


def add_new_worker():
    """
    In this window the manager can provide the details of the worker,ID,password,Name,Secret word
    """
    # Window Layout:
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
    # Window Layout Conditions,according to button clicked by user:
    while True:
        add_new_worker_event_check = True
        add_new_worker_event, add_new_worker_values = add_new_worker_window.read()
        if add_new_worker_event == 'Add':
            input_ID = add_new_worker_values['input_ID']
            input_password = add_new_worker_values['input_password']
            input_name = add_new_worker_values['input_name']
            input_secret_word = add_new_worker_values['input_secret_word']
            if input_ID in db.worker_dict:
                add_new_worker_window["Error"].update("ID already exist")
                add_new_worker_event_check = False
            elif input_ID in db.student_dict:
                add_new_worker_window["Error"].update("ID is registered as student")
                add_new_worker_event_check = False
            else:
                db.addWorker(Worker(str(input_ID), str(input_password), input_name, input_secret_word))
        if add_new_worker_event == sg.WIN_CLOSED or add_new_worker_event == "Exit" or (
                add_new_worker_event == "Add" and add_new_worker_event_check):
            add_new_worker_window.close()
            break


def remove_worker(chosen_worker_id):
    """Function for removing a workers from the system"""
    # Window Layout:
    remove_worker_layout = [
        [sg.Text("Are you sure you want to remove this worker?")],
        [sg.Button(button_text="Yes"),
         sg.Button(button_text="No"), ]]
    remove_worker_window = sg.Window("Remove Worker", remove_worker_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        remove_worker_event, remove_worker_values = remove_worker_window.read()
        if remove_worker_event == 'Yes':
            db.worker_dict.pop(chosen_worker_id)
            db.updateWorkers()
        if remove_worker_event == sg.WIN_CLOSED or remove_worker_event == "Yes" or remove_worker_event == "No":
            remove_worker_window.close()
            break


def remove_item():
    """This function allows the manager to remove items from the system"""
    # Window Layout:
    remove_worker_layout = [
        [sg.Text("Are you sure you want to remove this item?")],
        [sg.Button(button_text="Yes"),
         sg.Button(button_text="No"), ]]
    remove_worker_window = sg.Window("Remove Item", remove_worker_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        remove_worker_event, remove_worker_values = remove_worker_window.read()
        if remove_worker_event == sg.WIN_CLOSED or remove_worker_event == "Yes" or remove_worker_event == "No":
            remove_worker_window.close()
            break


def open_backlog(input_event_personas='StudentsLog'):
    """
    Using this functionality the manager can view a log of logins into the system by different users
    """
    # Window Layout:
    open_backlog_headings = ['ID', 'Name', 'Login dates:']
    backlog_list = None
    if input_event_personas == "StudentsLog":
        backlog_list = db.student_backlog

    elif input_event_personas == "WorkersLog":
        backlog_list = db.worker_backlog

    open_backlog_values = backlog_list
    open_backlog_layout = [[sg.Table(values=open_backlog_values,
                                     headings=open_backlog_headings,
                                     auto_size_columns=False,
                                     display_row_numbers=False,
                                     justification='c',
                                     num_rows=10,
                                     key='-TABLE-',
                                     row_height=35,
                                     col_widths=[15, 15, 25],
                                     enable_events=True, )],
                           [sg.Text(size=(30, 1), key="Error")],
                           [sg.Button('Students Log', size=(10, 1), key='students_log'),
                            sg.Button('Workers Log', size=(10, 1), key='workers_log'),
                            sg.Exit(pad=((380, 0), (0, 0)))]]
    open_backlog_window = sg.Window("Backlog", open_backlog_layout, element_justification='c', size=(700, 470))
    # Window Layout Conditions,according to button clicked by user:
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
    """Using this functioality the manager can edit item details,such like:Name,Quantity,Description,Due Date,Due Acquired"""
    # Window Layout:
    edit_items_layout = [
        [sg.Text('Item Name:')],
        [sg.InputText('', size=(20, 1), key='<item_name>')],
        [sg.Text('Item Quantity:')],
        [sg.InputText('', size=(20, 1), key='<item_quantity>')],
        [sg.Text('Item Description:')],
        [sg.InputText('', size=(20, 1), key='<item_Description>>')],
        [sg.Text('Due Date:')],
        [sg.InputText('', size=(20, 1), key='<item_Date>>')],
        [sg.Text('Loan Date:')],
        [sg.InputText('', size=(20, 1), key='<item_Acquired>>')],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Confirm', size=(10, 1)),
         sg.Button('Exit', size=(10, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    edit_items_layout_window = sg.Window("Edit Items", edit_items_layout, element_justification='c', size=(250, 450))
    # Window Layout Conditions,according to button clicked by user:
    while True:
        add_items_layout_event, edit_items_layout_values = edit_items_layout_window.read()
        if add_items_layout_event == sg.WIN_CLOSED or add_items_layout_event == "Exit":
            break

    edit_items_layout_window.close()


def open_manager_window(current_worker):
    """The main manager window in the system,allows him the following:
    Adding and removing items
    Editing item details
    Managing workers,adding new ones and removing existing ones
    Viewing a backlog of user logins into the system
    """
    # Window Layout:
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = db.getAvailableItemTable()
    open_manager_layout = [
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
         sg.Button('Manage Workers', size=(15, 1)),
         sg.Button('Backlog', size=(15, 1)),
         sg.Exit(pad=((0, 0), (0, 0)))]
    ]

    manager_window = sg.Window("manager Menu", open_manager_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
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

        if open_manager_event == "Remove":
            remove_item()

        if open_manager_event == sg.WIN_CLOSED or open_manager_event == "Exit":
            manager_window.close()
            break
