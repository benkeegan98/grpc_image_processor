import unittest
import pathlib
import grpc
from concurrent import futures

from PIL import Image

import image_pb2_grpc, image_pb2
from server import ImageServiceServicer

class TestImageServer(unittest.TestCase):

    def setUp(self):
        self.parent_path = pathlib.Path(__file__).parent.parent.resolve()
        test_img = Image.open(str(self.parent_path) + '/test_images/test-png.png')
        self.test_img = image_pb2.Image(color=True, data=test_img.tobytes(), width=test_img.size[0], height=test_img.size[1])
        self.service = ImageServiceServicer()

    def run_rotation_test(self, rotation_string, expected_image_path):
        expected_img = Image.open(str(self.parent_path) + expected_image_path)
        rotate_request = image_pb2.ImageRotateRequest(rotation=rotation_string, image=self.test_img)
        response = self.service.RotateImage(rotate_request, None)
        self.assertEqual(response.data, expected_img.tobytes())

    def run_mean_rotation_test(self, rotation_string, expected_image_path):
        expected_img = Image.open(str(self.parent_path) + expected_image_path)
        rotate_request = image_pb2.ImageRotateRequest(rotation=rotation_string, image=self.test_img)
        rotate_response = self.service.RotateImage(rotate_request, None)
        response = self.service.MeanFilter(rotate_response, None)
        self.assertEqual(response.data, expected_img.tobytes())
    
    def test_rotate_image_ninety(self):
        self.run_rotation_test('NINETY_DEG', '/test_images/rotated-90-test-png.png')

    def test_rotate_image_one_eighty(self):
        self.run_rotation_test('ONE_EIGHTY_DEG', '/test_images/rotated-180-test-png.png')

    def test_rotate_image_two_seventy(self):
        self.run_rotation_test('TWO_SEVENTY_DEG', '/test_images/rotated-270-test-png.png')

    def test_mean_filter(self):
        expected_mean_img = Image.open(str(self.parent_path) + '/test_images/mean-test-png.png')
        response = self.service.MeanFilter(self.test_img, None)
        self.assertEqual(response.data, expected_mean_img.tobytes())

    def test_rotate_ninety_mean(self):
        self.run_mean_rotation_test('NINETY_DEG', '/test_images/rotate-90-mean-test-png.png')

    def test_rotate_one_eighty_mean(self):
        self.run_mean_rotation_test('ONE_EIGHTY_DEG', '/test_images/rotate-180-mean-test-png.png')

    def test_rotate_two_seventy_mean(self):
        self.run_mean_rotation_test('TWO_SEVENTY_DEG', '/test_images/rotate-270-mean-test-png.png')


        