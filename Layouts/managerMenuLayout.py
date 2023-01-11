import PySimpleGUI as sg
from DataBase import db
from Personas import Item, Worker
from Layouts import registerLayout


# to do : complete this func , func is called in add_item func
def add_item_check(input_name, input_quantity, input_description):
    return True


def add_item():
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


# do this func
def edit_item(current_item):
    """Using this functionality the manager can edit item details,such like:Name,Description,Due Date,
    Date Acquired """
    # Window Layout:
    edit_items_layout = [
        [sg.Text('Item Name:')],
        [sg.InputText('', size=(20, 1), key='item_name')],
        [sg.Text('Item Description:')],
        [sg.InputText('', size=(20, 1), key='item_description')],
        [sg.Text('Loan Date:')],
        [sg.InputText('', size=(20, 1), key='aq_Date')],
        [sg.Text('Due Date:')],
        [sg.InputText('', size=(20, 1), key='du_Date')],
        [sg.Text(size=(10, 0), key="Error"), ],
        [sg.Button('Confirm', size=(10, 1)),
         sg.Button('Exit', size=(10, 1)),
         sg.Exit(pad=((50, 0), (50, 0)))]]
    edit_items_window = sg.Window("Edit Items", edit_items_layout, element_justification='c', size=(250, 450))
    # Window Layout Conditions,according to button clicked by user:
    while True:
        edit_item_event, edit_item_values = edit_items_window.read()
        input_name = edit_item_values['item_name']
        input_description = edit_item_values['item_description']
        input_aq_date = edit_item_values['aq_Date']
        input_du_date = edit_item_values['du_Date']

        if edit_item_event == 'Confirm':
            if input_name != '' or input_description != '' or input_aq_date != '' or input_du_date != '':
                if input_name == '':
                    input_name = current_item.name
                if input_description == '':
                    input_description = current_item.description
                if input_aq_date == '':
                    input_aq_date = current_item.aq_date
                if input_du_date == '':
                    input_du_date = current_item.du_date
                current_item.name = input_name
                current_item.description = input_description
                current_item.aq_date = input_aq_date
                current_item.du_date = input_du_date
                db.updateItems()
                edit_items_window.close()
                break
            else:
                edit_items_window["Error"].update("No Input Data")

        if edit_item_event == sg.WIN_CLOSED or edit_item_event == "Exit":
            edit_items_window.close()
            break


def remove_item(chosen_item_id):
    """This function allows the manager to remove items from the system"""
    # Window Layout:
    remove_item_layout = [
        [sg.Text("Are you sure you want to remove this item?")],
        [sg.Button(button_text="Yes"),
         sg.Button(button_text="No"), ]]
    remove_item_window = sg.Window("Remove Item", remove_item_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        remove_item_event, remove_item_values = remove_item_window.read()

        if remove_item_event == 'Yes':
            db.item_dict.pop(chosen_item_id)
            db.updateItems()
            remove_item_window.close()
            break

        if remove_item_event == sg.WIN_CLOSED or remove_item_event == "No":
            remove_item_window.close()
            break


def add_worker():
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
                              sg.Exit(pad=((250, 0), (0, 0)))]]

    add_worker_window = sg.Window("Add New Worker", add_new_worker_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        add_worker_event, add_worker_values = add_worker_window.read()
        if add_worker_event == 'Add':
            input_ID = add_worker_values['input_ID']
            input_password = add_worker_values['input_password']
            input_name = add_worker_values['input_name']
            input_secret_word = add_worker_values['input_secret_word']
            if input_ID != '' and input_password != '' and input_name != '' and input_secret_word != '':
                if input_ID in db.worker_dict.keys():
                    add_worker_window["Error"].update("ID already exist")
                elif input_ID in db.student_dict.keys():
                    add_worker_window["Error"].update("ID is registered as student")
                else:
                    db.addWorker(Worker(str(input_ID), str(input_password), input_name, input_secret_word))
                    add_worker_window.close()
                    break
            else:
                add_worker_window["Error"].update("One or more of the fields are empty")
        if add_worker_event == sg.WIN_CLOSED or add_worker_event == "Exit":
            add_worker_window.close()
            break


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
         sg.Exit(pad=((150, 0), (0, 0)))]]
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
                check_info = True
                db.updateWorkers()
            elif Password != '' and Secret_Word == '':
                db.worker_dict[chosen_worker_id].password = Password
                check_info = True
                db.updateWorkers()
            elif Password == '' and Secret_Word != '':
                db.worker_dict[chosen_worker_id].secret_word = Secret_Word
                check_info = True
                db.updateWorkers()
            else:
                edit_worker_window["Error"].update("No Input Data")
        if edit_worker_event == sg.WIN_CLOSED or (
                edit_worker_event == "Confirm" and check_info) or edit_worker_event == "Exit":
            edit_worker_window.close()
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
            remove_worker_window.close()
            break
        if remove_worker_event == sg.WIN_CLOSED or remove_worker_event == 'No':
            remove_worker_window.close()
            break


def edit_student(chosen_student_id):
    """Function for edit a student's info"""
    # Window Layout:
    edit_student_layout = [
        [sg.Text('New Password:')],
        [sg.InputText('', size=(20, 1), key='<Password>')],
        [sg.Text('New Secret Word:')],
        [sg.InputText('', size=(20, 1), key='<Secret_Word>')],
        [sg.Text(size=(10, 0), key="Error")],
        [sg.Button('Confirm', size=(10, 1)),
         sg.Exit(pad=((50, 0), (00, 0)))]]
    edit_student_window = sg.Window("Edit Student", edit_student_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        check_info = False
        edit_student_event, edit_student_values = edit_student_window.read()
        Password = edit_student_values['<Password>']
        Secret_Word = edit_student_values['<Secret_Word>']
        if edit_student_event == 'Confirm':
            if Password != '' and Secret_Word != '':
                db.student_dict[chosen_student_id].password = Password
                db.student_dict[chosen_student_id].secret_word = Secret_Word
                check_info = True
                db.updateStudents()
            elif Password != '' and Secret_Word == '':
                db.student_dict[chosen_student_id].password = Password
                check_info = True
                db.updateStudents()
            elif Password == '' and Secret_Word != '':
                db.student_dict[chosen_student_id].secret_word = Secret_Word
                check_info = True
                db.updateStudents()
            else:
                edit_student_window["Error"].update("No Input Data")
        if edit_student_event == sg.WIN_CLOSED or (
                edit_student_event == "Confirm" and check_info) or edit_student_event == "Exit" or edit_student_event == sg.WIN_CLOSED:
            edit_student_window.close()
            break


def remove_student(chosen_student_id):
    """Function for removing a students from the system"""
    # Window Layout:
    remove_student_layout = [
        [sg.Text("Are you sure you want to remove this student?")],
        [sg.Button(button_text="Yes"),
         sg.Button(button_text="No"), ]]
    remove_student_window = sg.Window("Remove Student", remove_student_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        remove_student_event, remove_student_values = remove_student_window.read()
        if remove_student_event == 'Yes':
            db.student_dict.pop(chosen_student_id)
            db.updateStudents()
        if remove_student_event == sg.WIN_CLOSED or remove_student_event == "Yes" or remove_student_event == "No":
            remove_student_window.close()
            break


def manage_workers():
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
         sg.Exit(pad=((165, 0), (0, 0)))]
    ]
    manage_workers_window = sg.Window("Manage Workers", manage_workers_layout)
    # Window Layout Conditions,according to button clicked by user:
    while True:
        manage_workers_event, manage_workers_values = manage_workers_window.read()
        if manage_workers_event == "Add New Worker":
            if manage_workers_event == "Add New Worker":
                add_worker()

        if manage_workers_event == "Remove Worker":
            if manage_workers_values['-TABLE-']:
                if len(manage_workers_values['-TABLE-']) == 1:
                    chosen_worker_idx = manage_workers_values['-TABLE-'][0]
                    chosen_worker_id = current_workers[chosen_worker_idx][1]
                    remove_worker(chosen_worker_id)
                    manage_workers_window.close()
                    manage_workers()
                else:
                    manage_workers_window["Error"].update("multiple Workers Selected !")
            else:  # warning if the user didn't select worker
                manage_workers_window["Error"].update("No worker Selected !")

        if manage_workers_event == "Edit Worker":
            if manage_workers_values['-TABLE-']:
                if len(manage_workers_values['-TABLE-']) == 1:
                    chosen_worker_idx = manage_workers_values['-TABLE-'][0]
                    chosen_worker_id = current_workers[chosen_worker_idx][1]
                    edit_worker(chosen_worker_id)
                    manage_workers_window.close()
                    manage_workers()
                else:
                    manage_workers_window["Error"].update("multiple Workers Selected !")
            else:  # warning if the user didn't select worker
                manage_workers_window["Error"].update("No Worker Selected !")

        elif manage_workers_event == "Exit" or manage_workers_event == sg.WIN_CLOSED:
            manage_workers_window.close()
            break


def manage_students():
    """
       Using this functionality the manager can View a list of all the students in the system and add or remove students
       """
    # Window Layout:
    current_students = db.getStudents()
    manage_students_headings = ['Name', 'ID']
    manage_students_layout = [
        [sg.Table(values=current_students,
                  headings=manage_students_headings,
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35,
                  def_col_width=25,
                  enable_events=True, )],
        [sg.Text(size=(15, 1), key="Error")],
        [sg.Button('Add New Student', size=(15, 1)),
         sg.Button('Remove Student', size=(15, 1)),
         sg.Button('Edit Student', size=(15, 1)),
         sg.Exit(pad=((165, 0), (0, 0)))]
    ]
    manage_students_window = sg.Window("Manage Students", manage_students_layout)
    # Window Layout Conditions,according to button clicked by user:
    while True:
        manage_students_event, manage_students_values = manage_students_window.read()

        if manage_students_event == "Add New Student":
            registerLayout.open_register_window()
            manage_students_window.close()
            manage_students()

        if manage_students_event == "Remove Student":
            if manage_students_values['-TABLE-']:
                if len(manage_students_values['-TABLE-']) == 1:
                    chosen_student_idx = manage_students_values['-TABLE-'][0]
                    chosen_student_id = current_students[chosen_student_idx][1]
                    remove_student(chosen_student_id)
                    manage_students_window.close()
                    manage_students()
                else:
                    manage_students_window["Error"].update("multiple Students Selected !")
            else:  # warning if the user didn't select student
                manage_students_window["Error"].update("No student Selected !")

        if manage_students_event == "Edit Student":
            if manage_students_values['-TABLE-']:
                if len(manage_students_values['-TABLE-']) == 1:
                    chosen_student_idx = manage_students_values['-TABLE-'][0]
                    chosen_student_id = current_students[chosen_student_idx][1]
                    edit_student(chosen_student_id)
                    manage_students_window.close()
                    manage_students()
                else:
                    manage_students_window["Error"].update("multiple Students Selected !")
            else:  # warning if the user didn't select student
                manage_students_window["Error"].update("No student Selected !")

        elif manage_students_event == "Exit" or manage_students_event == sg.WIN_CLOSED:
            manage_students_window.close()
            break


def open_manager_window():
    """The main manager window in the system,allows him the following:
    Adding and removing items
    Editing item details
    Managing workers,adding new ones and removing existing ones
    Viewing a backlog of user logins into the system
    """
    # Window Layout:
    current_inventory_headings = ['ID', 'Item', 'Owner', 'Status', 'Loan Date', 'Due Date', 'Loan Period (weeks)',
                                  'Description', 'Rating']
    current_inventory = db.getAvailableItemTable_forManager()
    manager_menu_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='c',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True)],
        [sg.Text(size=(30, 0), key="Error"), ],
        [sg.Button('Add', size=(15, 1)),
         sg.Button('Remove', size=(15, 1)),
         sg.Button('Edit', size=(15, 1)),
         sg.Button('Manage Workers', size=(15, 1)),
         sg.Button('Manage Students', size=(15, 1)),
         sg.Button('Backlog', size=(15, 1)),
         sg.Exit(pad=((0, 0), (0, 0)))]
    ]

    manager_window = sg.Window("manager Menu", manager_menu_layout, element_justification='c')
    # Window Layout Conditions,according to button clicked by user:
    while True:
        manager_menu_event, manager_menu_values = manager_window.read()

        if manager_menu_event == "Backlog":
            open_backlog()
        if manager_menu_event == "Add":
            add_item()
            manager_window.close()
            open_manager_window()

        if manager_menu_event == "Edit":
            if manager_menu_values['-TABLE-']:
                if len(manager_menu_values['-TABLE-']) == 1:
                    chosen_item_idx = manager_menu_values['-TABLE-'][0]
                    chosen_item_id = current_inventory[chosen_item_idx][0]
                    edit_item(db.item_dict[chosen_item_id])
                    manager_window.close()
                    open_manager_window()
                else:
                    manager_window["Error"].update("Can't edit multiple items at once")
            else:  # error to user if he didn't choose item
                manager_window["Error"].update("No Items selected")

        if manager_menu_event == "Manage Workers":
            manage_workers()

        if manager_menu_event == "Remove":
            if manager_menu_values['-TABLE-']:
                if len(manager_menu_values['-TABLE-']) == 1:
                    chosen_item_idx = manager_menu_values['-TABLE-'][0]
                    chosen_item_id = current_inventory[chosen_item_idx][0]
                    remove_item(chosen_item_id)
                    manager_window.close()
                    open_manager_window()
                else:
                    manager_window["Error"].update("Can't remove multiple items at once")
            else:  # error to user if he didn't choose item
                manager_window["Error"].update("No Items selected")

        if manager_menu_event == "Manage Students":
            manage_students()

        if manager_menu_event == sg.WIN_CLOSED or manager_menu_event == "Exit":
            manager_window.close()
            break
