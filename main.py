import PySimpleGUI as sg

layout = [[sg.Text("Hello and welcome to the design department inventory management system !")],
          [sg.Text("Username :")],
          [sg.InputText()],
          [sg.Text("Password :")],
          [sg.InputText()],
          [sg.Submit(), sg.Exit()],
          ]

# Create the window
window = sg.Window("Inventory Management System ", layout, )

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the Exit button
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
