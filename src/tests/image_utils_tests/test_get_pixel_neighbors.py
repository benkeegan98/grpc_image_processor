import unittest
import sys
sys.path.append("..")

from PIL import Image

from utils.image_utils import get_pixels_buffer, get_pixel_neighbors

class TestGetPixelNeighbors(unittest.TestCase):

    def setUp(self):
        self.width, self.height = 20, 20

    def assertExpectedNeighbors(self, neighbors, expected_neighbors):
        self.assertEqual(len(neighbors), len(expected_neighbors))
        for neighbor in expected_neighbors:
            self.assertIn(neighbor, neighbors)

    def test_internal_pixel(self):

        expected_neighbors = [(9,9), (10,9), (11,9), (9,10), (11,10), (9,11), (10,11), (11,11)]

        x, y = 10, 10
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_top_left_corner_pixel(self):

        expected_neighbors = [(0,1), (1,1), (1,0)]

        x, y = 0, 0
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_top_right_corner_pixel(self):

        expected_neighbors = [(18,0), (18,1), (19,1)]

        x, y = 19, 0
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)
    
    def test_bottom_left_corner_pixel(self):

        expected_neighbors = [(0,18), (1,18), (1,19)]

        x, y = 0, 19
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_bottom_right_corner_pixel(self):

        expected_neighbors = [(18,18), (19,18), (18,19)]

        x, y = 19, 19
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_top_edge_pixel(self):

        expected_neighbors = [(9,0), (9,1), (10,1), (11,0), (11,1)]

        x, y = 10, 0
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_bottom_edge_pixel(self):

        expected_neighbors = [(9,18), (9,19), (10,18), (11,18), (11,19)]

        x, y = 10, 19
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)
    
    def test_left_edge_pixel(self):

        expected_neighbors = [(0,9), (1,9), (1,10), (0,11), (1,11)]

        x, y = 0, 10
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)

    def test_right_edge_pixel(self):

        expected_neighbors = [(19, 9), (18, 9), (19, 11), (18, 11), (18, 10)]

        x, y = 19, 10
        neighbors = get_pixel_neighbors(x, y, self.width, self.height)

        self.assertExpectedNeighbors(neighbors, expected_neighbors)