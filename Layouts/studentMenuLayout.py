import PySimpleGUI as sg
import database_Personas
import main


def open_student_window():
    headings = ['Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']
    info = list(main.db.item_dict.values())
    info = main.db.getItemTable()
    student_menu_layout = [
        [sg.Table(values=info,
                  headings=headings,
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
            break
        if student_menu_event == "My Items" or student_menu_event == sg.WIN_CLOSED:
            break

        if student_menu_event == sg.WIN_CLOSED or student_menu_event == "Exit":
            student_menu_window.close()
            break
