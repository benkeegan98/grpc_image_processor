import unittest
import sys
sys.path.append("..")

import image_pb2
from utils.image_utils import is_valid_image

class TestIsValidImage(unittest.TestCase):

    def test_valid_image(self):

        expected = True

        data = b'\xff' * 1024
        width = 16
        height = 64
        color = False

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_zero_length_data(self):
        expected = False

        data = b''
        width = 16
        height = 64
        color = True

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_data_exceeds_max_length(self):
        expected = False

        data = b'\xff' * 4194305
        width = 16
        height = 64
        color = True

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_zero_height_image(self):
        expected = False

        data = b'\xff' * 1024
        width = 16
        height = 0
        color = False

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_zero_width_image(self):
        expected = False

        data = b'\xff' * 1024
        width = 0
        height = 64
        color = False

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_negative_height_image(self):
        expected = False

        data = b'\xff' * 1024
        width = 16
        height = -10
        color = False

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)

    def test_negative_width_image(self):
        expected = False

        data = b'\xff' * 1024
        width = -16
        height = 64
        color = False

        image = image_pb2.Image(color=color, data=data, width=width, height=height)

        self.assertEqual(is_valid_image(image), expected)
