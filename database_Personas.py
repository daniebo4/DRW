import os

class Student:
    def __init__(self, name, password, ID, secret_word):
        self.name = name
        self.password = password
        self.ID = ID
        self.secret_word = secret_word.replace("\n", "")


class Worker:
    def __init__(self, name, password, ID, secret_word):
        self.name = name
        self.password = password
        self.ID = ID
        self.secret_word = secret_word.replace("\n", "")

'''
class Manager:
    def __init__(self, username, password, ID, secret_word):
        self.username = username
        self.password = password 
        self.ID = ID  
        self.secret_word = secret_word.replace("\n", "") 
'''


class Data_base:
    # Databases are text files , following lines translate the data to dictionaries for easier access and manipulation
    def __init__(self,file_dir_s,file_dir_w):
        with open(file_dir_s, 'r') as file: # Students database
            student_list = file.readlines()
            student_list = list(map(lambda x: x.split(":"), student_list))
            student_list = list(map(lambda x: Student(x[0], x[1], x[2], x[3]), student_list))
            self.student_dict = {s.ID: s for s in student_list}


        with open(file_dir_w, 'r+') as file2: # Workers database
            worker_list = file2.readlines()
            if os.path.getsize(file_dir_w) == 0:
                file2.write("admin:admin:admin:admin\n")
            worker_list = list(map(lambda x: x.split(":"), worker_list))
            worker_list = list(map(lambda x: Worker(x[0], x[1], x[2], x[3]), worker_list))
            self.worker_dict = {w.ID: w for w in worker_list}
