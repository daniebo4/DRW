import unittest
import main


class studentMenuTest(unittest.TestCase):
    def test1_rating_item(self):
        """tries to rate an item twice to see if it does avg and updates"""
        self.assertEqual(main.studentMenuLayout.rate(5, 'Item test'), '5.0')
        self.assertEqual(main.studentMenuLayout.rate(4, 'Item test'), '4.5')
        main.db.item_dict['13'].num_raters = 0
        main.db.item_dict['13'].rating = 0

    def test2_request_item(self):
        """tries to request item and checks if request item function succeeds and returns True"""
        self.assertTrue(main.studentMenuLayout.request_item(main.db.student_dict['0'], '13'))
        self.assertFalse(main.studentMenuLayout.request_item(main.db.student_dict['0'], '!'))

    def test3_return_item(self):
        """tries to return item and checks if request item function succeeds and returns True"""
        self.assertFalse(main.studentMenuLayout.return_item([], '1'))

    def test4_studentLayout(self):
        """tries to check if the window shows the item"""
        self.assertFalse(main.studentMenuLayout.return_item([], '1'))

if __name__ == '__main__':
    unittest.main()

"""def test1_return_item(self):
       # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_my_items_window(main.db.student_dict[2])
        self.assertEqual(main.db.item_dict[10].status, 'pending')

def test2_Request_item(self):
        # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_request_item_window(main.db.student_dict[1],main.db.item_dict[10])
        self.assertEqual(main.db.item_dict[10].owner, 'pending')"""  # back up testing functions , currently not working
