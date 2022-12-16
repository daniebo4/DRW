import PySimpleGUI as sg
from database_Personas import DataBase
import main
import os


# remove current student parameter to rating functions ?
# make rating not possible after student already rated item
def rate(rating, item_name):
    for item in main.db.item_dict.values():
        if item_name == item.name:
            temp_item_num_raters = float(item.num_raters)
            temp_item_num_raters += 1
            item.rating = str(
                round((((float(item.rating) * (temp_item_num_raters - 1)) + rating) / temp_item_num_raters), 2))
            item.num_raters = str(temp_item_num_raters)
    item_file = main.project_root_dir + '\\Items_data.txt'
    item_rating_temp = ""
    with open(item_file, 'w+') as file:
        for i in main.db.item_dict.values():
            item_rating_temp=i.rating
            file.write(
                f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                f"{i.num_raters}:{i.owner}:{i.status}\n")
    return item_rating_temp


    main.db = DataBase(main.project_root_dir + '\\Students_data.txt',
                       main.project_root_dir + '\\Workers_data.txt',
                       main.project_root_dir + '\\Items_data.txt')


def open_rate_window(current_student, item_name):
    rate_layout = [[sg.Text("Rate Item")],
                   [sg.Button('1', size=(4, 1)), sg.Button('2', size=(4, 1)), sg.Button('3', size=(4, 1)),
                    sg.Button('4', size=(4, 1)), sg.Button('5', size=(4, 1))],
                   ]

    rate_window = sg.Window("Rate Menu", rate_layout, element_justification='c')
    while True:
        rate_event, rate_values = rate_window.read()

        if isinstance(rate_event, str):
            rate(int(rate_event), item_name)
            rate_window.close()
            break

        if rate_event == sg.WIN_CLOSED:
            rate_window.close()
            break


def open_my_items_window(current_student):
    my_items_headings = ['ID', 'Name', 'Loan Date', 'Due Date', 'Description', 'Rating', 'status']
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
                  row_height=35,
                  enable_events=True, )],
        [sg.Button('Return', size=(15, 1)),
         sg.Text(size=(15, 1), key="Error"),
         sg.Exit(pad=((300, 0), (0, 0)))]
    ]

    my_items_window = sg.Window("My Items", my_items_layout)
    while True:
        my_items_event, my_items_values = my_items_window.read()
        if my_items_event == 'Return':
            if len(my_items_values['-TABLE-']) > 0:
                item_idx = my_items_values['-TABLE-']
                item_id = []

                for index, item in enumerate(student_loaned_items):
                    if index in item_idx:
                        item_id.append(item[0])

                for ID in item_id:
                    main.db.item_dict[ID].status = 'pending'

                item_file = main.project_root_dir + '\\Items_data.txt'
                with open(item_file, 'w') as file:
                    for i in main.db.item_dict.values():
                        file.write(
                            f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                            f"{i.num_raters}:{i.owner}:{i.status}\n")

                main.db = DataBase(main.project_root_dir + '\\Students_data.txt',
                                   main.project_root_dir + '\\Workers_data.txt',
                                   main.project_root_dir + '\\Items_data.txt')
                my_items_window.close()
                open_my_items_window(current_student)
            else:
                my_items_window["Error"].update("No item selected !")
        if my_items_event == "Exit" or my_items_event == sg.WIN_CLOSED:
            my_items_window.close()
            break


def open_request_item_window(current_student, item_id):
    # make function work with multiple items
    student_loaned_items = main.db.get_students_loaned_items(current_student)
    request_item_layout = [
        [sg.Text("Are you sure you want to loan ?")],
        [sg.Button('Yes', ),
         sg.Button('No', )]
        # add return date please
    ]

    request_item_window = sg.Window("Request Item", request_item_layout)

    while True:
        request_item_event, request_item_values = request_item_window.read()
        if request_item_event == "Yes":
            main.db.item_dict[item_id].owner = current_student.ID
            item_file = main.project_root_dir + '\\Items_data.txt'
            with open(item_file, 'w+') as file:
                for i in main.db.item_dict.values():
                    file.write(
                        f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:"
                        f"{i.rating}:{i.num_raters}:{i.owner}:{i.status}\n")

            request_item_window.close()
            break
        if request_item_event == "No" or request_item_event == sg.WIN_CLOSED:
            request_item_window.close()
            break
    request_item_window.close()


def open_student_window(current_student):
    current_inventory_headings = ['ID', 'Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    current_inventory = main.db.getAvailableItemTable()
    student_menu_layout = [
        [sg.Table(values=current_inventory,
                  headings=current_inventory_headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=False,
                  justification='l',
                  num_rows=10,
                  key='-TABLE-',
                  row_height=35, enable_events=True)],
        [sg.Button('Request Item', size=(15, 1)),
         sg.Button('My Items', size=(15, 1)),
         sg.Button('Rate', size=(15, 1)),
         sg.Text(size=(30, 1), key="Error"),
         sg.Exit(pad=((0, 0), (0, 0)))]
    ]

    student_menu_window = sg.Window("Student Menu", student_menu_layout, element_justification='c')
    while True:
        student_menu_event, student_menu_values = student_menu_window.read()
        student_menu_window["Error"].update("")

        if student_menu_event == "Request Item":
            if student_menu_values['-TABLE-']:
                # insert if condition multiple item selection
                if len(student_menu_values['-TABLE-']) == 1:
                    item_idx = student_menu_values['-TABLE-'][0]
                    item_id = current_inventory[item_idx][0]
                    open_request_item_window(current_student, item_id)
                student_menu_window.close()
                open_student_window(current_student)
            else:
                student_menu_window["Error"].update("No Items selected")

        if student_menu_event == "My Items":
            open_my_items_window(current_student)

        if student_menu_event == "Rate":
            if len(student_menu_values['-TABLE-']) == 1:
                item_idx = student_menu_values['-TABLE-'][0]
                item_name = current_inventory[item_idx][1]
                open_rate_window(current_student, item_name)
                student_menu_window.close()
                open_student_window(current_student)
            elif len(student_menu_values['-TABLE-']) > 1:
                student_menu_window["Error"].update("You can only rate one item at a time")
            else:
                student_menu_window["Error"].update("choose item to rate!")

        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
