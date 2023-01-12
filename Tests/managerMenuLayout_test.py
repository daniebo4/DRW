import unittest
import DataBase
from Personas import Item
from Personas import Worker, Student
from Layouts import managerMenuLayout, registerLayout

class managerMenuTest(unittest.TestCase):

    def test1_add_item(self):
        """Checks if adding items to the system works properly"""
        self.assertFalse(managerMenuLayout.add_item_check('Test', -1 ,'Test'))
        self.assertTrue(managerMenuLayout.add_item_check('Test', 1 ,'Test'))
        self.assertEqual(managerMenuLayout.add_item_func('9999','Test', 1, 'Test', 'Test'),
                         "Item was successfully added to database :)")
        DataBase.db.item_dict.pop('9999')
        DataBase.db.updateItems()

    def test2_remove_item(self):
        """Checks if removing items from the system works properly"""
        testItem = Item("9999", "TEST", "", "", "TESTING", '0', '0', '0', "available", "0")
        DataBase.db.addItem(testItem)
        self.assertTrue(managerMenuLayout.remove_item_func(testItem.ID))
        if '9999' in DataBase.db.file_dir_item:
            DataBase.db.item_dict.pop(testItem.ID)
            DataBase.db.updateItems()

    def test3_add_worker(self):
        """Checks if adding workers to the system works properly"""
        self.assertEqual(managerMenuLayout.add_worker_func('9999','test', 'test', 'secret-test'), "Worker was successfully added to database XD")
        # removes test worker from database after test is done
        if '9999' in DataBase.db.file_dir_worker:
            DataBase.db.worker_dict.pop('9999')
            DataBase.db.updateWorkers()

    def test4_remove_worker(self):
        """Checks if removing workers from the system works properly"""
        testWorker = Worker("9999", "test-password", "Test Worker", "quite secretive-word")
        DataBase.db.addWorker(testWorker)
        DataBase.db.updateItems()
        self.assertEqual(managerMenuLayout.remove_worker_func('9999'), "Worker was successfully removed from database")
        if '9999' in DataBase.db.file_dir_worker:
            DataBase.db.worker_dict.pop('9999')
            DataBase.db.updateWorkers()

    def test5_add_student(self):
        """Checks if adding students to the system works properly"""
        self.assertTrue(registerLayout.check_register("9999", 'test', 'test', 'secret-test'))
        # removes test student from database after test is done
        if '9999' in DataBase.db.file_dir_student:
            DataBase.db.student_dict.pop('9999')
            DataBase.db.updatestudents()

    def test6_remove_student(self):
        """Checks if removing students from the system works properly"""
        test_student = Student ("9999", "test-password", "Test student", "quite secretive-word")
        DataBase.db.addstudent(test_student)
        DataBase.db.updateItems()
        self.assertEqual(managerMenuLayout.remove_student_func('9999'), "Student was removed successfully from database")
        if '9999' in DataBase.db.file_dir_student:
            DataBase.db.student_dict.pop(test_student.ID)
            DataBase.db.updatestudents()

    def test7_edit_worker(self):
        """Checks if editing worker info in the system works properly"""
        testWorker = Worker("9999", "bad-pass", "Test Worker", "quite secretive-word")
        DataBase.db.addWorker(testWorker)
        DataBase.db.updateItems()
        self.assertEqual(managerMenuLayout.edit_worker_func("9999", 'good-pass', 'much more secretive-word'),
                         "Worker was edited successfully,cheers!")
        # removes test student from database after test is done
        if '9999' in DataBase.db.file_dir_worker:
            DataBase.db.student_dict.pop('9999')
            DataBase.db.updatestudents()

    def test8_edit_item(self):
        """Checks if editing item info in the system works properly"""
        testItem = Item("9999", "TEST1", "", "", "TESTING", '0', '0', '0', "available", "0")
        DataBase.db.addItem(testItem)
        self.assertEqual(managerMenuLayout.edit_item_func("9999", 'test2', '', '', ''),
                         "Item was successfully edited, nice")
        # removes test item from database after test is done
        if '9999' in DataBase.db.file_dir_item:
            DataBase.db.student_dict.pop('9999')
            DataBase.db.updatestudents()


if __name__ == '__main__':
    unittest.main()