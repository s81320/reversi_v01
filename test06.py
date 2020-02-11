# run as pytest test06.py

from unittest import TestCase
from unittest.mock import patch, Mock

import take06 as reversi

class TestObjectCreation(TestCase):

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

	def test_check_position_exists(self):
		mock_host = Mock(spec=reversi.Host)
		b = reversi.Board(mock_host)
		self.assertEqual(b.check_position_exists((9,9)), False)
		self.assertEqual(b.check_position_exists((3,19)), False)
		self.assertEqual(b.check_position_exists((13,4)), False)
		self.assertEqual(b.check_position_exists((9,'a')), False)
		self.assertEqual(b.check_position_exists(('+','a')), False)

		self.assertEqual(b.check_position_exists((1,2)), True)
		self.assertEqual(b.check_position_exists((7,5)), True)
		self.assertEqual(b.check_position_exists((0,0)), True)
		self.assertEqual(b.check_position_exists((2,4)), True)
		self.assertEqual(b.check_position_exists((5,7)), True)

	def test_creation_host(self):
		pass

	def test_creation_player(self):
		pass	
