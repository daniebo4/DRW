import os
from Personas import Student, Worker, Item
from itertools import chain
import datetime


class DataBase:
    """
    Creates a new class database of work which contains the personas of the system.
    Databases are text files , following lines translate the data to dictionaries for easier access and manipulation.
    """

    def __init__(self, file_dir_student=None, file_dir_worker=None, file_dir_item=None,
                 file_dir_student_backlog=None, file_dir_worker_backlog=None, file_dir_design_students=None):
        self.file_dir_student_backlog = file_dir_student_backlog
        self.file_dir_worker_backlog = file_dir_worker_backlog
        self.file_dir_student = file_dir_student
        self.file_dir_worker = file_dir_worker
        self.file_dir_item = file_dir_item
        self.file_dir_design_students = file_dir_design_students
        if file_dir_student:
            with open(file_dir_student, 'r') as file:  # Students database
                """opens the file of the student to read and create a list from"""
                student_list = file.readlines()
                student_list = list(map(lambda x: x.split(":"), student_list))
                student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
                self.student_dict = {s.ID: s for s in student_list}
        if file_dir_worker:
            with open(file_dir_worker, 'r+') as file2:  # Workers database
                worker_list = file2.readlines()
                if os.path.getsize(file_dir_worker) == 0:
                    file2.write("admin:admin:admin:admin\n")
                worker_list = list(map(lambda x: x.split(":"), worker_list))
                worker_list = list(map(lambda x: Worker(x[0], x[1], x[2], x[3]), worker_list))
                self.worker_dict = {w.ID: w for w in worker_list}
        if file_dir_item:
            with open(file_dir_item, 'r') as file3:  # Items database
                item_list = file3.readlines()
                item_list = list(map(lambda x: x.split(":"), item_list))
                # items in database are separated as such-ID:name:date aq:date due:
                # description:rating:num_raters:owner:status
                item_list = list(
                    map(lambda x: Item(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]), item_list))
                self.item_dict = {i.ID: i for i in item_list}
        if file_dir_student_backlog:
            with open(file_dir_student_backlog, 'r') as file4:
                self.student_backlog = list(map(lambda x: x.split(":"), file4.read().splitlines()))
        if file_dir_worker_backlog:
            with open(file_dir_worker_backlog, 'r') as file5:
                self.worker_backlog = list(map(lambda x: x.split(":"), file5.read().splitlines()))
        if file_dir_design_students:
            with open(file_dir_design_students, 'r') as file6:
                self.design_students_list = file6.read().splitlines()

    def getAvailableItemTable(self):
        """get the items that are in the database and puts in a list for tables to show the items"""
        item_list_to_print = []
        item_table_amount_dict = {}
        # calculate quantity of items to be displayed
        for item in self.item_dict.values():
            # '0' means that currently the item has no owner
            if item.owner in (None, "", '0'):
                if item.name not in item_table_amount_dict:
                    item_table_amount_dict[item.name] = 1
                else:
                    item_table_amount_dict[item.name] += 1

        # creates table of items to be displayed
        items_in_table = set()
        for item in self.item_dict.values():
            if item.name in item_table_amount_dict and item.owner in (None, "", '0'):
                items_in_table.add(item.name)
                current_item = [item.ID, item.name, item_table_amount_dict[item.name],
                                item.aq_date, item.du_date, item.description, item.rating]
                item_list_to_print.append(current_item)
        return item_list_to_print

    def getAvailableItemTable_forMenu(self):
        """this gets the available items like the one above but there are small changes
         in the table because we want to show the user what the loan period"""
        item_table_amount_dict = {}
        for item in self.item_dict.values():  # calculate quantity of items to be displayed
            if item.owner in (None, "", '0'):  # '0' means that currently the item has no owner
                if item.name not in item_table_amount_dict:
                    item_table_amount_dict[item.name] = 1
                else:
                    item_table_amount_dict[item.name] += 1

        item_list_to_print = []
        for item in self.item_dict.values():
            if item.name in item_table_amount_dict and item.name not in chain(*item_list_to_print):
                current_item = [item.name, item_table_amount_dict[item.name],
                                item.loan_period, item.rating, item.description]
                item_list_to_print.append(current_item)
        return item_list_to_print

    def get_students_loaned_items(self, current_student):
        """gets the items that belong to a student by going into
        the database and looking for the owner in the item data to see if the students owns it"""
        item_list_to_print = []
        for item in self.item_dict.values():
            if item.owner == current_student.ID:
                current_item = [item.ID, item.name, item.aq_date, item.du_date, item.description, item.rating,
                                item.status]
                item_list_to_print.append(current_item)
        return item_list_to_print

    # for worker menu :
    def get_loan_requested_items(self):
        item_list_to_print = []
        for item in self.item_dict.values():
            if item.status == 'loan requested':
                current_item = [item.ID, item.name, item.description, item.rating,
                                item.status, item.owner, self.student_dict[item.owner].ID]
                item_list_to_print.append(current_item)
        return item_list_to_print

    def get_return_requested_items(self):
        item_list_to_print = []
        for item in self.item_dict.values():
            if item.status == 'return requested':
                current_item = [item.ID, item.name, item.description, item.rating,
                                item.status, item.owner, self.student_dict[item.owner].ID]
                item_list_to_print.append(current_item)
        return item_list_to_print

    def addStudent(self, student_obj):
        with open(self.file_dir_student, 'a') as file:
            file.write(f"{student_obj.ID}:{student_obj.password}:{student_obj.name}:{student_obj.secret_word}\n")
        db.student_dict[student_obj.ID] = student_obj

    def updateStudents(self):
        with open(self.file_dir_student, 'w') as file:
            for s in self.student_dict.values():
                file.write(f"{s.ID}:{s.password}:{s.name}:{s.secret_word}\n")

    def addItem(self, item_obj):
        with open(self.file_dir_item, 'a') as file:
            file.write(f"{item_obj.ID}:{item_obj.name}:{item_obj.aq_date}:{item_obj.du_date}:"
                       f"{item_obj.description}:{item_obj.rating}:{item_obj.num_raters}:{item_obj.owner}"
                       f":{item_obj.status}:{item_obj.loan_period}\n")
        db.item_dict[item_obj.ID] = item_obj

    def updateItems(self):
        with open(self.file_dir_item, 'w') as file:
            for i in db.item_dict.values():
                file.write(
                    f"{i.ID}:{i.name}:{i.aq_date}:{i.du_date}:{i.description}:{i.rating}:"
                    f"{i.num_raters}:{i.owner}:{i.status}:{i.loan_period}\n")

    def check_login_student(self, input_ID, input_password):
        """a function that checks if student`s ID and password are matching"""
        return input_ID in self.student_dict and self.student_dict[input_ID].password == input_password

    def check_login_worker(self, input_ID, input_password):
        """a function that checks if worker`s ID and password are matching"""
        return input_ID in self.worker_dict and self.worker_dict[input_ID].password == input_password

    def updateWorkers(self):
        with open(self.file_dir_worker, 'w') as file:
            for s in self.worker_dict.values():
                file.write(f"{s.ID}:{s.password}:{s.name}:{s.secret_word}\n")

    def addWorker(self, worker_obj):
        with open(self.file_dir_worker, 'a') as file:
            file.write(f"{worker_obj.ID}:{worker_obj.password}:{worker_obj.name}:{worker_obj.secret_word}\n")
        db.worker_dict[worker_obj.ID] = worker_obj

    def addToStudentBacklog(self, input_ID):
        new_entry = [self.student_dict[input_ID].ID, self.student_dict[input_ID].name, datetime.date.today()]
        self.student_backlog.append(new_entry)
        with open(self.file_dir_student_backlog, 'a') as file:
            file.write(
                f"{new_entry[0]}:{new_entry[1]}:{new_entry[2]}\n")

    def addToWorkerBacklog(self, input_ID):
        new_entry = [self.worker_dict[input_ID].ID, self.worker_dict[input_ID].name, datetime.date.today()]
        self.worker_backlog.append(new_entry)
        with open(self.file_dir_worker_backlog, 'a') as file:
            file.write(
                f"{new_entry[0]}:{new_entry[1]}:{new_entry[2]}\n")

    def getWorkers(self):
        worker_list=[]
        for worker in self.worker_dict.values():
            if worker.ID != 'admin':
                worker_list.append([worker.name,worker.ID])
        return worker_list

    def getStudents(self):
        student_list=[]
        for student in self.student_dict.values():
            student_list.append([student.name,student.ID])
        return student_list


project_root_dir = os.path.dirname(os.path.abspath(__file__)) + '\\Data'  # Finds path to current project folder
db = DataBase(project_root_dir + '\\Students_data.txt',
              project_root_dir + '\\Workers_data.txt',
              project_root_dir + '\\Items_data.txt',
              project_root_dir + '\\BackLogDatabaseStudents.txt',
              project_root_dir + '\\BackLogDatabaseWorkers.txt',
              project_root_dir + '\\DesignDepartmentStudent.txt')
