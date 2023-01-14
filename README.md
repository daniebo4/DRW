# DRW

Welcome to DRW, an inventory management system.   
DRW allows users to easily manage any type of inventory.   
A python project created to satisfy the needs of students in the design 
department for better managed inventory system in collages.   
Main features: item management, item loans and returns, users management.     

## How to use:

DRW is a storage system made for the students of SCE design department where student can ask
to loan out items and workers and managers are in charge of handling requests.

Students: In order to access the student menu the student must first be in the database of students that are
in the design department, after that they must register and choose their name, password and secret word.
After logining into the system they will be greeted with a student menu where they can see all the available items that are available to loan.
After choosing with the left click mouse they can request an item to loan, by requesting a loan request will be sent out to the
worker and will need to be accepted for the student to acquire the item.
After the item has been accepted the student can go into his inventory and left click and return the item when he's finished.
At the end of the item return the student will get a popup message that will ask him to rate the item.
The student is able to use forgot password and change password.

Worker: In order to access the system first the manger has to add the worker in the database through his add worker menu
after a successful login the worker can see the items that are currently available to loan and
can manage return and request by all the students in the department.
The worker can also change and use forget password.

Manager: System default for manager login is the ID-admin and password-admin and once he logs in he can add item to the inventory by pressing add.
He can also edit by pressing on an item and hitting edit.
He can remove items  by pressing remove, he can add,edit,remove workers and students.
He also can watch a backlog of student and worker logins.

## Installation

1.Install Python 3.11.1.     
2.Install Py Charm.       
3.In PyCharm's terminal, run the command 'pip install pysimplegui' in order to install PySimpleGUI.      
3.Open main.py using Py Charm.    
4.Run main.py in Py Charm.     


```bash
pip install pysimplegui
```


## Contributing

Lior Abergel , Daniel Borisenko, Maor Merling, Elad Levi

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.




