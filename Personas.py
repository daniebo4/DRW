import os
import datetime
from importlib import reload

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


