import unittest

import forgotPasswordLayout


class forgotPasswordTest(unittest.TestCase):
    def setUp(self): pass
    def test_getPassword(self):
        self.assertIsNone(forgotPasswordLayout.get_forgot_password())

