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
		self.assertEqual(b.maxNumberStones,64)
		self.assertIsInstance(b.board,dict)
		self.assertEqual(len(b.board), b.maxNumberStones)

	def test_creation_host(self):
		pass

	def test_creation_player(self):
		pass	


	#def setUp(self):
	#	mock_board = Mock(spec=reversi.Board)


	#def test_check_position_exists(self, position):
    #    """Returns True iff (position) is on the board."""
    #    #print("in Brett : check position exists")
    #    return (position[0] in range(self.size)) and (position[1] in range(self.size))