from unittest import TestCase

from clgridworld.wrapper.euclidean_distance_calculator import EuclideanDistanceCalculator


class TestEuclideanDistanceCalculator(TestCase):

    def test_distance_between_0_0_and_10_10(self):

        starting_point = (0, 0)
        ending_point = (10, 10)

        actual = EuclideanDistanceCalculator.distance(starting_point, ending_point)

        expected = 14.14
        self.assertAlmostEqual(expected, actual, places=2)