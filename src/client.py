import sys
import logging
import grpc
from PIL import Image

import image_pb2, image_pb2_grpc

import utils.argument_parser as argument_parser
import utils.image_utils as image_utils

def rotate_image(stub, image, rotation):
    '''
    Makes call to RotateImage method in ImageService server, and returns value from this endpoint

        Parameters:
            stub (ImageServiceStub): Stub for connecting to grpc ImageService server
            image (Image): Image object to rotate
            rotation (str): ImageRotateRequest.Rotation Enum string representing rotation type
        Returns:
            (Image): Image of rotated image
    '''
    image_rotate_request = image_pb2.ImageRotateRequest(rotation=rotation, image=image)
    return stub.RotateImage(image_rotate_request)

def mean_filter(stub, image):
    '''
    Makes call to MeanFilter method in ImageService server, and returns value from this endpoint

        Parameters:
            stub (ImageServiceStub): Stub for connecting to grpc ImageService server
            image (Image): Image object representing image of which to apply mean filter
        Returns:
            (Image): Image object of mean filtered image argument
    '''
    return stub.MeanFilter(image)


def run():
    '''
    Runs client.py.

    Parses and validates arguments passed into client.py. If arguments are invalid, ArgumentParser.error() is triggered.
    Arguments are invalid if:
        - Both --rotate and --mean flags are omitted.
        - --input or --output arguments are not valid .png, .jpg, or .jpeg file paths.
        - --port is an invalid port number.
    Connects client ImageServiceStub to ImageService service if host and port form correct address, otherwise exits and logs error.
    If connection is made, Image is created from input image, endpoints are called on this Image, and result is saved to output path.
    '''
    args_parser = argument_parser.get_client_args_parser()
    args = args_parser.parse_args()

    if args.rotate is None and args.mean is False:
        args_parser.error("Cannot omit both --rotate and --mean flags - at least one must be present")
    if not args.input.lower().endswith(('.png', '.jpg', '.jpeg')):
        args_parser.error("Invalid input - image file must have extension .png, .jpg, or .jpeg")
    if not args.output.lower().endswith(('.png', '.jpg', '.jpeg')):
        args_parser.error("Invalid output - file path must have extension .png, .jpg, or .jpeg")
    if not args.port.isdigit() or int(args.port) > 65535:
        args_parser.error("Invalid port number " + args.port + " - use a positive integer value less than 65535")

    try:
        with grpc.insecure_channel(args.host + ':' + args.port) as channel:
            stub = image_pb2_grpc.ImageServiceStub(channel)

            img = Image.open(args.input)
            image = image_utils.pil_image_to_image(img)

            if args.mean:
                image = mean_filter(stub, image)
            
            if args.rotate in image_pb2.ImageRotateRequest.Rotation.keys():
                image = rotate_image(stub, image, args.rotate)
        
            image_utils.save_image(image, args.output)
    except Exception:
        logging.error("Failed to connect to remote host: Connection refused - incorrect address")
        sys.exit(1)

if __name__ == '__main__':
    run()