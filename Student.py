class Student:
    def __init__(self, username, password, ID, secret_word):
        self.username = username
        self.password = password
        self.ID = ID
        self.secret_word = secret_word.replace("\n", "")