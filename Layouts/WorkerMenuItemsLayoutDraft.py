import PySimpleGUI as sg

Info = [
    ['Eraser', '10', '1914', '1919','Very nice and handy','$$$$'],
    ['Three Hole Punch', '5', '1965', '2025','Not enough holes','$$$$$'],
    ['Fine Brush', '2', '1988', '2001','Too Fine','$$'],
    ['Color Pallete', '5', '2002', '2002','Lots of colors','$$$'],
]

headings = ['Item', 'Quantity', 'Loan Date','Due Date','Description','Rating']

def add():
    return
def remove():
    return

layout = [
    [sg.Table(values=Info,
              headings=headings,
              max_col_width=25,
              auto_size_columns=True,
              display_row_numbers=False,
              justification='l',
              num_rows=10,
              key='-TABLE-',
              row_height=35)],
    [sg.Button('Add',),
    sg.Button('Remove', ),
    sg.Button('Requests',),
    sg.Button('Returns',),
    sg.Exit('Logout',pad=((450, 0), (0, 0)))]

]

window = sg.Window("Worker Menu", layout)

while True:
    event, values = window.read()
    if event == "Logout" or event == sg.WIN_CLOSED:
        break
    if event == "Add":
        add()
    if event == "Add":
        remove()


