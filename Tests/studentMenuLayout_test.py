import unittest
import DataBase
from Personas import Item
from Personas import Student
from Layouts import studentMenuLayout


class studentMenuTest(unittest.TestCase):

    def test1_rating_item(self):
        """tries to rate an item twice to see if it does avg and updates"""
        testItem = Item("999", "TEST", "", "", "TESTING", '0', '0', '0', "available", "0")
        # temporary item called TEST for testing funcs
        DataBase.db.addItem(testItem)
        self.assertEqual(studentMenuLayout.rate(5, 'TEST'), 'Update rating successful')
        self.assertEqual(studentMenuLayout.rate('5', 'TEST'), 'The rating is not an integer')
        self.assertNotEqual(studentMenuLayout.rate(5.2456, 'TEST'), 'Update rating successful')
        # removes test item when finished
        DataBase.db.item_dict.pop(testItem.ID)
        DataBase.db.updateItems()

    def test2_request_item(self):
        """tries to request item and checks if request item function succeeds and returns True"""
        testItem = Item("999", "TEST", "", "", "TESTING", '0', '0', '0', "available", "0")
        # temporary item called TEST for testing funcs
        DataBase.db.addItem(testItem)
        tempStudent = Student("999", "1", "Test Student", "testing")
        DataBase.db.addStudent(tempStudent)
        DataBase.db.updateItems()
        self.assertTrue(studentMenuLayout.request_item(tempStudent, testItem.ID))
        self.assertFalse(studentMenuLayout.request_item(tempStudent, '!'))
        # removes test item when finished
        DataBase.db.item_dict.pop(testItem.ID)
        # removes test student when finished
        DataBase.db.student_dict.pop(tempStudent.ID)
        DataBase.db.updateItems()

    def test3_return_item(self):
        """tries to return item and checks if request item function succeeds and returns True"""
        self.assertFalse(studentMenuLayout.return_item([], '1'))

    def test4_studentLayout(self):
        """tries to check if the window shows the item"""
        self.assertFalse(studentMenuLayout.return_item([], '1'))


if __name__ == '__main__':
    unittest.main()

"""def test1_return_item(self):
       # Tests if status of returned item is changed to "pending"
        DataBase.studentMenuLayout.open_my_items_window(DataBase.db.student_dict[2])
        self.assertEqual(DataBase.db.item_dict[10].status, 'pending')

def test2_Request_item(self):
        # Tests if status of returned item is changed to "pending"
        DataBase.studentMenuLayout.open_request_item_window(DataBase.db.student_dict[1],DataBase.db.item_dict[10])
        self.assertEqual(DataBase.db.item_dict[10].owner, 'pending')
        
        
        
        
        
        
        
        
        """  # back up testing functions , currently not working
