import PySimpleGUI as sg

Info = [
    ['Eraser', '10', '1914', '1919', 'Very nice and handy', '$$$$'],
    ['Three Hole Punch', '5', '1965', '2025', 'Not enough holes', '$$$$$'],
    ['Fine Brush', '2', '1988', '2001', 'Too Fine', '$$'],
    ['Color Pallet', '5', '2002', '2002', 'Lots of colors', '$$$'],
]

headings = ['Item', 'Quantity', 'Loan Date', 'Due Date', 'Description', 'Rating']


def open_student_window():
    layout = [
        [sg.Table(values=Info,
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

    window = sg.Window("Student Menu", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Request Item" or event == sg.WIN_CLOSED:
            break
        if event == "My Items" or event == sg.WIN_CLOSED:
            break


open_student_window()
