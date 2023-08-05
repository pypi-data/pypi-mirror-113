import unittest

from src.pbp import functions


class TestPBP(unittest.TestCase):
	def test_load(self):
		pbp = functions.load_pbp([2019])

		actual_shape = pbp.shape
		expected_shape = (38151, 372)
		self.assertEqual(actual_shape, expected_shape)

	# TODO: write more unit tests for test_load. have to play around with the data to model expected behavior
	# 		so we can actually write the tests

if __name__ == '__main__':
	unittest.main()
