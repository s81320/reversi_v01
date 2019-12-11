# run test in cli or 

import unittest
import take06 as reversi

class TestObjectCreation(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass	

	def test_creation_host(self):
		h = reversi.Brett(4)
		self.assertEqual(h.maxNumberStones,16)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.maxNumberStones)

		h = reversi.Brett(5)
		self.assertEqual(h.maxNumberStones,25)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.maxNumberStones)

		h = reversi.Brett(10)
		self.assertEqual(h.maxNumberStones,100)
		self.assertIsInstance(h.brett,dict)
		self.assertEqual(len(h.brett), h.maxNumberStones)

	def test_creation_board(self):
		pass

	def test_creation_player(self):
		pass	


if __name__ == '__main__':
    unittest.main()