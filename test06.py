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
		b = reversi.Board(mock_host, 4)
		self.assertEqual(b.maxNumberStones,16)
		self.assertIsInstance(b.board,dict)
		self.assertEqual(len(b.board), b.maxNumberStones)

	def test_creation_host(self):
		pass

	def test_creation_player(self):
		pass	
