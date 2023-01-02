import os
import datetime


class Student:
    def __init__(self, ID, password, name, secret_word):
        self.ID = ID
        self.password = password
        self.name = name
        self.secret_word = secret_word.replace("\n", "")


class Worker:
    def __init__(self, ID, password, name, secret_word):
        self.ID = ID
        self.password = password
        self.name = name
        self.secret_word = secret_word.replace("\n", "")


'''
class Manager:
    def __init__(self, ID, password, name, secret_word):
        self.ID = ID
        self.password = password
        self.name = name
        self.secret_word = secret_word.replace("\n", "")
'''  # class manager in case needed


class Item:
    """
    A class for the items that the storage has which has different parameters representing the item
    """

    def __init__(self, ID=None, name=None, aq_date=None, du_date=None, description=None, rating=0, num_raters=0,
                 owner=None, status=None, loan_period=None):
        self.ID = ID
        self.name = name
        self.description = description

        if aq_date != "":
            aq_date = aq_date.split("-")
            self.aq_date = datetime.date(int(aq_date[0]), int(aq_date[1]), int(aq_date[2]))
        else:
            self.aq_date = aq_date

        if du_date != "":
            du_date = du_date.split("-")
            self.du_date = datetime.date(int(du_date[0]), int(du_date[1]), int(du_date[2]))
        else:
            self.du_date = du_date

        self.rating = rating
        self.owner = owner
        self.status = status
        self.num_raters = num_raters
        self.loan_period = loan_period.replace("\n", "")


class DataBase:
    """
    Creates a new class database of work which contains the personas of the system.
    Databases are text files , following lines translate the data to dictionaries for easier access and manipulation.
    """

    def __init__(self, file_dir_student=None, file_dir_worker=None, file_dir_item=None):
        with open(file_dir_student, 'r') as file:  # Students database
            """opens the file of the student to read and create a list from"""
            student_list = file.readlines()
            student_list = list(map(lambda x: x.split(":"), student_list))
            student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
            self.student_dict = {s.ID: s for s in student_list}

        with open(file_dir_worker, 'r+') as file2:  # Workers database
            worker_list = file2.readlines()
            if os.path.getsize(file_dir_worker) == 0:
                file2.write("admin:admin:admin:admin\n")
            worker_list = list(map(lambda x: x.split(":"), worker_list))
            worker_list = list(map(lambda x: Worker(x[0], x[1], x[2], x[3]), worker_list))
            self.worker_dict = {w.ID: w for w in worker_list}

        with open(file_dir_item, 'r') as file3:  # Items database
            item_list = file3.readlines()
            item_list = list(map(lambda x: x.split(":"), item_list))
            # items in database are separated as such-ID:name:date aq:date due:
            # description:rating:num_raters:owner:status
            item_list = list(map(lambda x: Item(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]), item_list))
            self.item_dict = {i.ID: i for i in item_list}

        # methods to update database

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
                                item.aq_date, item.loan_period, item.description, item.rating]
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
