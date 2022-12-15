import PySimpleGUI as sg
import main


def open_my_items_window(current_student):
    my_items_headings = ['ID', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating']
    student_loaned_items = main.db.get_students_loaned_items(current_student)
    my_items_layout = [
        [sg.Table(values=student_loaned_items,
                  headings=my_items_headings,
                  max_col_width=25,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35)],
        [sg.Button('Return', size=(15, 1)),
         sg.Exit(pad=((430, 0), (0, 0)))]
    ]

    my_items_window = sg.Window("My Items", my_items_layout)

    while True:
        my_items_event, my_items_values = my_items_window.read()
        if my_items_event == "Return" or my_items_event == sg.WIN_CLOSED:
            # call to return item function
            pass
        if my_items_event == "Exit" or my_items_event == sg.WIN_CLOSED:
            my_items_window.close()
            break


def open_request_item_window(current_student):
    request_item_layout = [
        [sg.Text("Are you Sure?")],
        [sg.Button('Yes', ),
         sg.Button('No', )]
        # add return date please
    ]

    request_item_window = sg.Window("Request Item", request_item_layout)

    while True:
        request_item_event, request_item_values = request_item_window.read()
        if request_item_event == "Yes" or request_item_event == sg.WIN_CLOSED:
            request_item_window.close()
            break
        if request_item_event == "No" or request_item_event == sg.WIN_CLOSED:
            pass


def open_student_window(current_student):
    current_inventory_headings = ['Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getItemTable()
    student_menu_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35)],
        [sg.Button('Request Item', size=(15, 1)),
         sg.Button('My Items', size=(15, 1)),
         sg.Exit(pad=((430, 0), (0, 0)))]
    ]

    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c')
    while True:
        student_menu_event, student_menu_values = student_menu_window.read()

        if student_menu_event == "Request Item" or student_menu_event == sg.WIN_CLOSED:
            open_request_item_window(current_student)

        if student_menu_event == "My Items" or student_menu_event == sg.WIN_CLOSED:
            open_my_items_window(current_student)

        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
