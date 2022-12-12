import unittest

import forgotPasswordLayout
import main


class GetPasswordTest(unittest.TestCase):
    def setUp(self):
        pass

    def test1_fields_not_entered(self):
        self.assertEqual(forgotPasswordLayout.get_forgot_password('1', '2', ''),
                         "One or more of the fields not entered")

    def test2_ID_not_only_digits(self):
        self.assertEqual(forgotPasswordLayout.get_forgot_password('a', 'a', 'a'), "ID can only contain numbers")

    def test3_correct_ID_and_password(self):
        if main.db.student_dict:
            s = list(main.db.student_dict.values())[0]
            if len(s.secret_word) == 1:
                incorrect_secret_word = s.secret_word + 1
            else:
                incorrect_secret_word = s.secret_word[0]
            self.assertEqual(forgotPasswordLayout.get_forgot_password(s.name, s.password, incorrect_secret_word),
                             "ID exists but name or secret word do not")

    def test4_correct_ID_and_secret_word(self):
        if len(main.db.student_dict) > 0:
            s = list(main.db.student_dict.values())[0]
            incorrect_password = s.password[0]
            self.assertEqual(forgotPasswordLayout.get_forgot_password(s.name, incorrect_password, s.secret_word),
                             "ID exists but name or secret word do not")

    def test5_ID_not_correct(self):
        self.assertEqual(forgotPasswordLayout.get_forgot_password('', 'a', 'a'), "ID doesn't exists")


if __name__ == '__main__':
    unittest.main()
