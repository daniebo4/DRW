import PySimpleGUI as sg
import main

Info = [
    ['Eraser', '10', '1914', '1919','Very nice and handy','$$$$'],
]

headings = ['Item', 'Quantity', 'Loan Date','Due Date','Description','Rating']

def MyItems_window():
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
        [sg.Button('Return',size=(15, 1)),
        sg.Exit(pad=((430, 0), (0, 0)))]

    ]

    window = sg.Window("My Items", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Return" or event == sg.WIN_CLOSED:
            break

MyItems_window()
