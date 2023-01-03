import sys
import logging
from concurrent import futures
import grpc

import image_pb2, image_pb2_grpc
import utils.argument_parser as argument_parser
import utils.image_utils as image_utils

class ImageServiceServicer(image_pb2_grpc.ImageServiceServicer):
    '''
    Provides methods that implement functionality of image_pb2_grpc.ImageServiceServicer.

    ...

    Methods
    -------
    RotateImage(request, context):
        Rotates and returns Image.
    MeanFilter(request, context):
        Applies mean filter to and returns Image.
    '''

    def RotateImage(self, request, context):
        '''
        Rotates and returns Image.

        If Image is invalid, function exits and logs error.
        Provides server-side validation of rotation string, if invalid, function exits and logs error.
        Performs image rotation by copying individual pixels to new Image template.
        Returns rotated Image.
        '''

        if image_utils.is_valid_image(request.image):

            if request.rotation in image_pb2.ImageRotateRequest.Rotation.values():
        
                if request.rotation == image_pb2.ImageRotateRequest.Rotation.NONE:
                    return request.image
                else:

                    img = image_utils.image_to_pil_image(request.image)

                    width = request.image.width
                    height = request.image.height
                    if request.rotation in [image_pb2.ImageRotateRequest.Rotation.NINETY_DEG, image_pb2.ImageRotateRequest.Rotation.TWO_SEVENTY_DEG]:
                        width = request.image.height
                        height = request.image.width

                    new_img = image_utils.get_new_pil_image_template(request.image.data, width, height)

                    for x in range(request.image.width):
                        for y in range(request.image.height):
                            pixel_to_move = img.getpixel((x,y))

                            if request.rotation == image_pb2.ImageRotateRequest.Rotation.NINETY_DEG:
                                new_img.putpixel((width-y-1, x), pixel_to_move)
                            elif request.rotation == image_pb2.ImageRotateRequest.Rotation.ONE_EIGHTY_DEG:
                                new_img.putpixel((width-x-1, height-y-1), pixel_to_move)
                            elif request.rotation == image_pb2.ImageRotateRequest.Rotation.TWO_SEVENTY_DEG:
                                new_img.putpixel((y, height-x-1), pixel_to_move)
                    
                    data = new_img.tobytes()

                    return image_pb2.Image(color=request.image.color, data=data, width=width, height=height)
            else:
                logging.error('Invalid message - rotation string is not valid')
                sys.exit(1)
        else:
            logging.error('Invalid message - does not represent a valid image')
            sys.exit(1)

    def MeanFilter(self, request, context):
        '''
        Applies mean filter and returns Image.

        If Image is invalid, function exits and logs error.
        Applies mean filter, accounting for whether image is single channel greyscale, 3 channel 'RGB', or 4 channel 'RGBA'.
        Returns mean filtered Image.
        '''

        if image_utils.is_valid_image(request):

            img = image_utils.image_to_pil_image(request)
            pixels = image_utils.get_pixels_buffer(img)

            for x in range(request.width):
                for y in range(request.height):

                    neighbors = image_utils.get_pixel_neighbors(x, y, request.width, request.height)
                    neighbors.append((x,y))
                    neighbors = [pixels[x][y] for (x,y) in neighbors]

                    if request.color:
                        r = sum([rgb[0] for rgb in neighbors]) // len(neighbors)
                        g = sum([rgb[1] for rgb in neighbors]) // len(neighbors)
                        b = sum([rgb[2] for rgb in neighbors]) // len(neighbors)

                        if "A" in img.getbands():
                            a = sum([a for r,g,b,a in neighbors]) // len(neighbors)
                            img.putpixel((x,y), (r,g,b,a))
                        else:
                            img.putpixel((x,y), (r,g,b))
                    else:
                        l = sum([l for l in neighbors]) // len(neighbors)

                        img.putpixel((x,y), l)

            data = img.tobytes()

            return image_pb2.Image(color=request.color, data=data, width=request.width, height=request.height)
        else:
            logging.error('Invalid message - does not represent a valid image')
            sys.exit(1)

def serve():
    '''
    Runs server.py.

    Parses arguments passed into server.py. If --port is invalid, ArgumentParser.error() is triggered and program exits.
    Creates grpc server, adds ImageServiceServicer to server, and starts server at address formed by host and port arguments.
    '''
    args_parser = argument_parser.get_server_args_parser()
    args = args_parser.parse_args()

    if not args.port.isdigit() or int(args.port) > 65535:
        args_parser.error("Invalid port number " + args.port + " - use a positive integer value less than 65535")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_ImageServiceServicer_to_server(
        ImageServiceServicer(), server
    )
    server.add_insecure_port(args.host + ':' + args.port)
    server.start()
    server.wait_for_termination()
    

if __name__ == '__main__':
    serve()
