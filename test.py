# run as pytest test06.py

import unittest
from unittest.mock import Mock

import reversi

class TestObjectCreation(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_creation_board(self):
		mock_host = Mock(spec=reversi.Host)
		b = reversi.Board(mock_host)
		self.assertEqual(b.max_number_stones,64)
		self.assertIsInstance(b.board,dict)
		self.assertEqual(len(b.board), b.max_number_stones)

class TestBoardFunctions(unittest.TestCase):

	def test_check_position_exists(self):
		mock_host = Mock(spec=reversi.Host)
		b = reversi.Board(mock_host)
		self.assertEqual(b.check_position_exists((9, 9)), False)
		self.assertEqual(b.check_position_exists((3, 19)), False)
		self.assertEqual(b.check_position_exists((13, 4)), False)
		self.assertEqual(b.check_position_exists((9, 'a')), False)
		self.assertEqual(b.check_position_exists(('+', 'a')), False)

		self.assertEqual(b.check_position_exists((1, 2)), True)
		self.assertEqual(b.check_position_exists((7, 5)), True)
		self.assertEqual(b.check_position_exists((0, 0)), True)
		self.assertEqual(b.check_position_exists((2, 4)), True)
		self.assertEqual(b.check_position_exists((5, 7)), True)

	def test_create_directions_ingoing(self):
		mock_host = Mock(spec=reversi.Host)
		b = reversi.Board(mock_host)
		all_directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1))
		self.assertEqual(b.create_directions_ingoing((2,3)), all_directions)
		self.assertEqual(b.create_directions_ingoing((5,1)), all_directions)
		self.assertEqual(b.create_directions_ingoing((0,0)), ((1,0),(0,1),(1,1)))
		self.assertEqual(b.create_directions_ingoing((7,0)), ((-1,0),(0,1),(-1,1)))
		self.assertEqual(b.create_directions_ingoing((7,7)), ((-1,0),(0,-1),(-1,-1)))
		self.assertEqual(b.create_directions_ingoing((0,7)), ((1,0),(0,-1),(1,-1)))

	# def test_check_for_same_colour(self):
	# 	mock_host = Mock(spec=reversi.Host)
	# 	b = reversi.Board(mock_host)
	# 	# mock the Board.board ! needs to have values to be tested.
	# 	self.assertEqual(b.check_for_same_colour((4,2),(4,3)), True)

	def test_creation_host(self):
		pass

	def test_creation_player(self):
		pass

if __name__ == '__main__':
    unittest.main()
