import unittest
import main


class studentMenuLayout(unittest.TestCase):
    def test3_Rating_item(self):
        """tries to rate an item twice to see if it does avg and updates"""
        self.assertEqual(main.studentMenuLayout.rate(5, 'Item test'), '5.0')
        self.assertEqual(main.studentMenuLayout.rate(4, 'Item test'), '4.5')


if __name__ == '__main__':
    unittest.main()




"""def test1_return_item(self):
       # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_my_items_window(main.db.student_dict[2])
        self.assertEqual(main.db.item_dict[10].status, 'pending')"""

"""  def test2_Request_item(self):
        # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_request_item_window(main.db.student_dict[1],main.db.item_dict[10])
        self.assertEqual(main.db.item_dict[10].owner, 'pending')"""