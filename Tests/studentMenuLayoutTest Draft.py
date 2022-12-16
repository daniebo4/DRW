import unittest
import main


class studentMenuLayout(unittest.TestCase):
    def test1_return_item(self):
        # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_my_items_window(main.db.student_dict[2])
        self.assertEqual(main.db.item_dict[10].status, 'pending')

    def test2_Request_item(self):
        # Tests if status of returned item is changed to "pending"
        main.studentMenuLayout.open_request_item_window(main.db.student_dict[1],main.db.item_dict[10])
        self.assertEqual(main.db.item_dict[10].owner, 'pending')

    def test3_Rating_item(self):
        # draft
        main.studentMenuLayout.rate(main.db.student_dict[1] ,5, main.db.item_dict[10])
        self.assertEqual(((main.student_loaned_items[main.db.item_dict[10]].rating * (main.student_loaned_items[main.db.item_dict[10]].num_raters-1))+5)/(main.student_loaned_items[main.db.item_dict[10]].num_raters+1))

if __name__ == '__main__':
    unittest.main()
