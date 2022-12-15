import os


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
    def __init__(self, ID, name, description, rating, du_date=None, aq_date=None, owner=None, status=None):
        self.ID = ID
        self.name = name
        self.aq_date = aq_date
        self.du_date = du_date
        self.description = description
        self.rating = rating
        self.owner = owner
        self.status = status.replace("\n","")


class DataBase:
    # Databases are text files , following lines translate the data to dictionaries for easier access and manipulation
    def __init__(self, file_dir_student=None, file_dir_worker=None, file_dir_item=None):
        with open(file_dir_student, 'r') as file:  # Students database
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
            # items in database are separated as such - ID:name:date acquired:due date:description:rating
            item_list = list(map(lambda x: Item(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]), item_list))
            self.item_dict = {i.ID: i for i in item_list}

        # methods to update database

    def getItemTable(self):
        item_list_to_print = []
        item_table_amount_dict = {}
        for item in self.item_dict.values():
            if item.name not in item_table_amount_dict:
                item_table_amount_dict[item.name] = 1
            else:
                item_table_amount_dict[item.name] += 1

        items_in_table = set()
        for item in self.item_dict.values():
            if item.name not in items_in_table:
                items_in_table.add(item.name)
                current_item = [item.name, item_table_amount_dict[item.name],
                                item.aq_date, item.du_date, item.description, item.rating]
                item_list_to_print.append(current_item)
        return item_list_to_print

    def get_students_loaned_items(self, current_student):
        item_list_to_print = []
        for item in self.item_dict.values():
            if item.owner == current_student.ID:
                current_item = [item.ID, item.name, item.aq_date, item.du_date, item.description, item.rating,
                                item.status]
                item_list_to_print.append(current_item)
        return item_list_to_print
