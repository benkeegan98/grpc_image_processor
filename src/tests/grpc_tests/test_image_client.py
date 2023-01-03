import unittest
import pathlib
import grpc
from concurrent import futures

from PIL import Image

import image_pb2_grpc, image_pb2
from client import rotate_image, mean_filter
from server import ImageServiceServicer

class TestImageClient(unittest.TestCase):

    def setUp(self):
        self.parent_path = pathlib.Path(__file__).parent.parent.resolve()
        test_img = Image.open(str(self.parent_path) + '/test_images/test-png.png')
        self.test_img = image_pb2.Image(color=True, data=test_img.tobytes(), width=test_img.size[0], height=test_img.size[1])

        self.port = 50052
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        image_pb2_grpc.add_ImageServiceServicer_to_server(ImageServiceServicer(), self.server)
        self.server.add_insecure_port(f'localhost:{self.port}')
        self.server.start()

        channel = grpc.insecure_channel(f'localhost:{self.port}')
        self.stub = image_pb2_grpc.ImageServiceStub(channel)
    
    def tearDown(self):
        self.server.stop(None)

    def run_rotation_test(self, rotation_string, expected_image_path):
        expected_img = Image.open(str(self.parent_path) + expected_image_path)
        response = rotate_image(self.stub, self.test_img, rotation_string)
        self.assertEqual(response.data, expected_img.tobytes())

    def run_mean_rotation_test(self, rotation_string, expected_image_path):
        expected_img = Image.open(str(self.parent_path) + expected_image_path)
        rotate_response = rotate_image(self.stub, self.test_img, rotation_string)
        response = mean_filter(self.stub, rotate_response)
        self.assertEqual(response.data, expected_img.tobytes())

    def test_rotate_image_ninety(self):
        self.run_rotation_test('NINETY_DEG', '/test_images/rotated-90-test-png.png')

    def test_rotate_image_one_eighty(self):
        self.run_rotation_test('ONE_EIGHTY_DEG', '/test_images/rotated-180-test-png.png')

    def test_rotate_image_two_seventy(self):
        self.run_rotation_test('TWO_SEVENTY_DEG', '/test_images/rotated-270-test-png.png')

    def test_mean_filter(self):
        expected_mean_img = Image.open(str(self.parent_path) + '/test_images/mean-test-png.png')
        response = mean_filter(self.stub, self.test_img)
        self.assertEqual(response.data, expected_mean_img.tobytes())

    def test_rotate_ninety_mean(self):
        self.run_mean_rotation_test('NINETY_DEG', '/test_images/rotate-90-mean-test-png.png')

    def test_rotate_one_eighty_mean(self):
        self.run_mean_rotation_test('ONE_EIGHTY_DEG', '/test_images/rotate-180-mean-test-png.png')

    def test_rotate_two_seventy_mean(self):
        self.run_mean_rotation_test('TWO_SEVENTY_DEG', '/test_images/rotate-270-mean-test-png.png')

