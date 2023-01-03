import unittest
import sys
import pathlib
sys.path.append("..")

from PIL import Image

import image_pb2
from utils.image_utils import pil_image_to_image, image_to_pil_image

class TestPILImageToImage(unittest.TestCase):

    def test_valid_image_size(self):

        parent = pathlib.Path(__file__).parent.parent.resolve()
        file_path = '/test_images/test-jpg.jpg'
        img = Image.open(str(parent) + file_path)

        width, height = img.size
        data = img.tobytes()

        image = image_pb2.Image(color=True, data=data, width=width, height=height)

        self.assertEqual(pil_image_to_image(img), image)

    def test_image_exceeds_max_size(self):

        expected_error = 'Error: Image greater than max size of 4194304 bytes'

        parent = pathlib.Path(__file__).parent.parent.resolve()
        file_path = '/test_images/test-jpg-exceeds-max.jpeg'
        img = Image.open(str(parent) + file_path)

        with self.assertRaises(SystemExit) as ex:
            pil_image_to_image(img)

        self.assertEqual(ex.exception.code, expected_error)

class TestImageToPILImage(unittest.TestCase):

    def test_three_band_jpg(self):

        parent = pathlib.Path(__file__).parent.parent.resolve()
        file_path = '/test_images/test-jpg.jpg'
        img = Image.open(str(parent) + file_path)

        width, height = img.size
        data = img.tobytes()
        mode = 'RGB'
        img = Image.frombytes(mode, size=(width, height), data=data)

        image = image_pb2.Image(color=True, data=data, width=width, height=height)

        self.assertEqual(image_to_pil_image(image), img)

    def test_four_band_png(self):  

        parent = pathlib.Path(__file__).parent.parent.resolve()
        file_path = '/test_images/test-png.png'
        img = Image.open(str(parent) + file_path)

        width, height = img.size
        data = img.tobytes()
        mode = 'RGBA'
        img = Image.frombytes(mode, size=(width, height), data=data)
        
        image = image_pb2.Image(color=True, data=data, width=width, height=height)

        self.assertEqual(image_to_pil_image(image), img)

    def test_single_band(self):
        parent = pathlib.Path(__file__).parent.parent.resolve()
        file_path = '/test_images/test-jpg.jpg'
        img = Image.open(str(parent) + file_path).convert('L')

        width, height = img.size
        data = img.tobytes()
        mode = 'L'
        img = Image.frombytes(mode, size=(width, height), data=data)

        image = image_pb2.Image(color=True, data=data, width=width, height=height)

        self.assertEqual(image_to_pil_image(image), img)
