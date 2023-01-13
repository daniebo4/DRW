import unittest
from Layouts import registerLayout
import main


class RegisterTest(unittest.TestCase):
    """Test if one of fields is empty"""
    def test1_fields_not_entered(self):
        self.assertEqual(registerLayout.check_register('', '', '', ''),
                         registerLayout.register_errors[0])

    def test2_ID_illegal(self):
        """Tests ID illegal """
        self.assertEqual(registerLayout.check_register('289148353a', '123', 'aa', 'aa'),
                         registerLayout.register_errors[1])

    def test3_name_illegal(self):
        """Tests name contains digits"""
        self.assertEqual(registerLayout.check_register('289148353', '123', 'aa111', 'aa'),
                         registerLayout.register_errors[2])

    def test4_ID_exist(self):
        """Tests ID not exist in the department database"""
        if len(main.db.student_dict) > 0:
            self.assertEqual(registerLayout.check_register(list(main.db.student_dict.keys())[0],
                                                           '123', 'aa', 'aa'),
                             registerLayout.register_errors[4])

    def test5_ID_exist(self):
        """Tests ID already exist"""
        if len(main.db.student_dict) > 0:
            self.assertEqual(registerLayout.check_register(list(main.db.student_dict.keys())[1],
                                                           '123', 'aa', 'aa'),
                             registerLayout.register_errors[3])