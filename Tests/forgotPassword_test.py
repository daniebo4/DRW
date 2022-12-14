import unittest
from Layouts import forgotPasswordLayout
import main


class GetPasswordTest(unittest.TestCase):
    # Test fields not entered
    def test1_fields_not_entered(self):
        self.assertEqual(forgotPasswordLayout.get_forgot_password('1', '2', ''),
                         forgotPasswordLayout.errors[0])

    def test2_ID_not_only_digits(self):
        # Tests if ID is only digits
        self.assertEqual(forgotPasswordLayout.get_forgot_password('a', 'a', 'a'), "ID can only contain numbers")

    def test3_correct_ID_and_password(self):
        # Tests if ID and password match but secret word doesn't
        if main.db.student_dict:
            s = list(main.db.student_dict.values())[0]
            if len(s.secret_word) == 1:
                incorrect_secret_word = chr(ord(s.secret_word) + 1)
            else:
                incorrect_secret_word = s.secret_word[0]
            self.assertEqual(forgotPasswordLayout.get_forgot_password(s.name, s.password, incorrect_secret_word),
                             "ID exists but name or secret word do not")

    def test4_correct_ID_and_secret_word(self):
        # Tests if ID and secret word match but password doesn't
        if main.db.student_dict:
            s = list(main.db.student_dict.values())[0]
            if len(s.password) == 1:
                incorrect_password = chr(ord(s.password) + 1)
            else:
                incorrect_password = s.password[0]
            self.assertEqual(forgotPasswordLayout.get_forgot_password(s.name, incorrect_password, s.secret_word),
                             "ID exists but name or secret word do not")

    def test5_ID_not_correct(self):
        # Tests ID doesnt exists
        if main.db.student_dict:
            s = list(main.db.student_dict.values())[0]
            if len(s.ID) == 1:
                incorrect_ID = s.ID
                while incorrect_ID in main.db.student_dict:
                    incorrect_ID = chr(ord(incorrect_ID) + 1)
            else:
                incorrect_ID = s.ID[0]
            self.assertEqual(forgotPasswordLayout.get_forgot_password('a', incorrect_ID, 'a'), "ID doesn't exists")


if __name__ == '__main__':
    unittest.main()
