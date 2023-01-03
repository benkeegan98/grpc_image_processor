import unittest
import sys

from image_utils_tests.test_is_valid_image import TestIsValidImage
from image_utils_tests.test_pil_image_conversions import TestPILImageToImage, TestImageToPILImage
from image_utils_tests.test_get_pixel_neighbors import TestGetPixelNeighbors

from grpc_tests.test_image_server import TestImageServer
from grpc_tests.test_image_client import TestImageClient

unittest1 = unittest.TestLoader().loadTestsFromTestCase(TestIsValidImage)
unittest2 = unittest.TestLoader().loadTestsFromTestCase(TestPILImageToImage)
unittest3 = unittest.TestLoader().loadTestsFromTestCase(TestImageToPILImage)
unittest4 = unittest.TestLoader().loadTestsFromTestCase(TestGetPixelNeighbors)

servertest = unittest.TestLoader().loadTestsFromTestCase(TestImageServer)
clienttest = unittest.TestLoader().loadTestsFromTestCase(TestImageClient)

alltests = unittest.TestSuite([unittest1, unittest2, unittest3, unittest4, servertest, clienttest])

if __name__ == '__main__':
    unittest.main()

