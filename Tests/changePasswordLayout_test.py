import unittest
from Layouts import changePasswordLayout
import DataBase
class ChangePasswordTest(unittest.TestCase):
    def test1_fields_not_entered(self):
        """Test if one of fields is empty"""
        self.assertEqual(changePasswordLayout.attempt_to_change(' ', '   ', '1', ''),
                         changePasswordLayout.change_errors[0])
        self.assertEqual(changePasswordLayout.attempt_to_change('#@!$%', '   ', '1', ''),
                         changePasswordLayout.change_errors[0])

    def test2_id_is_digits(self):
        """Test if the ID isn't all numbers"""
        self.assertEqual(changePasswordLayout.attempt_to_change('abc', '1', '2', '2'),
                         changePasswordLayout.change_errors[1])
        self.assertEqual(changePasswordLayout.attempt_to_change('!cs1cx', '1', '2', '2'),
                         changePasswordLayout.change_errors[1])

    def test2_ID_incorrect_student(self):
        """Test if ID exists in student database"""
        if DataBase.db.student_dict:
            s = list(DataBase.db.student_dict.values())[0]
            if len(s.ID) == 1:
                incorrect_ID = s.ID
                while incorrect_ID in DataBase.db.student_dict:
                    incorrect_ID = chr(ord(incorrect_ID) + 1)
            else:
                incorrect_ID = s.ID[0]
            self.assertEqual(changePasswordLayout.attempt_to_change(incorrect_ID, 'a', 'a', 'a'),
                             changePasswordLayout.change_errors[2])

    def test3_current_password_incorrect(self):
        """Test if the current password doesn't match"""
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '4521', '3', '3'),
                         changePasswordLayout.change_errors[3])
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '!2!1', '3', '3'),
                         changePasswordLayout.change_errors[3])

    def test4_new_password_not_match(self):
        """Test if two new passwords input don't match (should be equal)"""
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '1', '5', '6'),
                         changePasswordLayout.change_errors[4])
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '1', 'sss', '55'),
                         changePasswordLayout.change_errors[4])

    def test5_ID_incorrect_worker_and_manager(self):
        """Test if ID exists in worker database"""
        if DataBase.db.worker_dict:
            s = list(DataBase.db.worker_dict.values())[1]
            if len(s.ID) == 1:
                incorrect_ID = s.ID
                while incorrect_ID in DataBase.db.worker_dict:
                    incorrect_ID = chr(ord(incorrect_ID) + 1)
            else:
                incorrect_ID = s.ID[0]
            self.assertEqual(changePasswordLayout.attempt_to_change(incorrect_ID, 'a', 'a', 'a'),
                             changePasswordLayout.change_errors[2])

    def test6_ID_incorrect_manager(self):
        """Test if manager exist in worker database"""
        if DataBase.db.worker_dict:
            s = list(DataBase.db.worker_dict.values())[0]
            if len(s.ID) == 1:
                incorrect_ID = s.ID
                while incorrect_ID in DataBase.db.worker_dict:
                    incorrect_ID = chr(ord(incorrect_ID) + 1)
            else:
                incorrect_ID = s.ID[0]
            self.assertEqual(changePasswordLayout.attempt_to_change(incorrect_ID, 'a', 'a', 'a'),
                             changePasswordLayout.change_errors[1])

if __name__ == '__main__':
    unittest.main()
