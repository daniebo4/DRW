import unittest
import changePasswordLayout
import main


class ChangePassword_test(unittest.TestCase):
    def test1_fields_not_entered(self):
        # Test if one of fields is empty
        self.assertEqual(changePasswordLayout.attempt_to_change(' ', '   ', '1', ''),
                         "One or more of the fields not entered")
        self.assertEqual(changePasswordLayout.attempt_to_change('#@!$%', '   ', '1', ''),
                         "One or more of the fields not entered")

    def test2_id_is_digits(self):
        # Test if the ID isn't all numbers
        self.assertEqual(changePasswordLayout.attempt_to_change('abc', '1', '2', '2'),
                         "ID can only contain numbers")
        self.assertEqual(changePasswordLayout.attempt_to_change('!cs1cx', '1', '2', '2'),
                         "ID can only contain numbers")

    def test3_current_password_incorrect(self):
        # Test if the current password doesn't match
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '4521', '3', '3'),
                         "Current password not correct")
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '!2!1', '3', '3'),
                         "Current password not correct")

    def test4_new_password_not_match(self):
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '1', '5', '6'),
                         "New passwords don't match")
        self.assertEqual(changePasswordLayout.attempt_to_change('1', '1', 'sss', '55'),
                         "New passwords don't match")




if __name__ == '__main__':
    unittest.main()
