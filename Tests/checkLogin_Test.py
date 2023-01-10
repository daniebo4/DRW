import unittest
import main
import DataBase


class LoginTest(unittest.TestCase):
    def test1_Matching_Credentials_Student_Database(self):
        """Tests function response when provided with valid and invalid credentials"""
        self.assertFalse(DataBase.db.check_login_student('$', '$'))
        self.assertTrue(DataBase.db.check_login_student('1', '1'))

    def test2_Matching_Credentials_Worker_Database(self):
        """Tests function response when provided with valid and invalid credentials"""
        self.assertFalse(DataBase.db.check_login_worker('$','$'))
        self.assertTrue(DataBase.db.check_login_worker('admin', 'admin'))

    def test3_OnlyOne_Matching_Credentials_Student_Database(self):
        """Tests function response when provided with only one valid and invalid credentials"""
        self.assertFalse(DataBase.db.check_login_student('1', '$'))

    def test4_OnlyOne_Matching_Credentials_Worker_Database(self):
        """Tests function response when provided with only one valid and invalid credentials"""
        self.assertFalse(DataBase.db.check_login_worker('$', 'admin'))

if __name__ == '__main__':
    unittest.main()
