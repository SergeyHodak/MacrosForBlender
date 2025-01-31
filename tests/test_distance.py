import unittest
from src.distance.distance import Distance

class TestDistance(unittest.TestCase):
    def setUp(self):
        self.calc = Distance()

    def test_get_2d_distance(self):
        test_list = [
            (5, [3, 4], [0, 0]),
            (1, [3, 0], [4, 0]),
            (5, [3, 0], [0, 4]),
            (5, [4, 3], [0, 0]),
            (1, [4, 0], [3, 0]),
            (5, [4, 0], [0, 3]),
            (5, [0, 3], [4, 0]),
            (1, [0, 3], [0, 4]),
            (5, [0, 4], [3, 0]),
            (5, [0, 0], [3, 4]),
            (1, [0, 4], [0, 3]),
            (5, [0, 0], [4, 3]),
            (5, [-3, 4], [0, 0]),
            (7, [-3, 0], [4, 0]),
            (5, [-3, 0], [0, 4]),
            (5, [4, -3], [0, 0]),
            (5, [0, -3], [4, 0]),
            (7, [0, -3], [0, 4]),
            (7, [4, 0], [-3, 0]),
            (5, [0, 4], [-3, 0]),
            (5, [0, 0], [-3, 4]),
            (5, [4, 0], [0, -3]),
            (7, [0, 4], [0, -3]),
            (5, [0, 0], [4, -3]),
            (5, [-4, 3], [0, 0]),
            (7, [-4, 0], [3, 0]),
            (5, [-4, 0], [0, 3]),
            (5, [3, -4], [0, 0]),
            (5, [0, -4], [3, 0]),
            (7, [0, -4], [0, 3]),
            (7, [3, 0], [-4, 0]),
            (5, [0, 3], [-4, 0]),
            (5, [0, 0], [-4, 3]),
            (5, [3, 0], [0, -4]),
            (7, [0, 3], [0, -4]),
            (5, [0, 0], [3, -4]),
            (5, [-3, -4], [0, 0]),
            (1, [-3, 0], [-4, 0]),
            (5, [-3, 0], [0, -4]),
            (5, [-4, -3], [0, 0]),
            (5, [0, -3], [-4, 0]),
            (1, [0, -3], [0, -4]),
            (1, [-4, 0], [-3, 0]),
            (5, [0, -4], [-3, 0]),
            (5, [0, 0], [-3, -4]),
            (5, [-4, 0], [0, -3]),
            (1, [0, -4], [0, -3]),
            (5, [0, 0], [-4, -3])
        ]
        for test in test_list:
            self.assertEqual(test[0], self.calc.get_2d_distance(test[1], test[2]))


if __name__ == '__main__':
    unittest.main()
