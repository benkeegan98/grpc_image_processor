import sys
import logging
from PIL import Image

import image_pb2

def is_valid_image(image):
    '''
    Returns True if Image is valid, False otherwise

    Will return False if image data has length 0, if image height or width is non-positive,
    or if image is greater than max size of 4194304 bytes

        Parameters:
            image (Image): Image object

        Returns:
            (bool): True or False representing Image validity
    '''
    if len(image.data) <= 0:
        return False
    elif len(image.data) > 4194304:
        return False
    elif image.width <= 0 or image.height <= 0:
        return False
    else:
        return True

def pil_image_to_image(img):
    '''
    Converts PIL Image object into Image object

    Constructs all fields necessary to initialize Image:
        Gets width and height of img.
        Sets color field to False if img is a single band greyscale image, or True if img has 3 (RGB) or 4 (RGBA) channels.
        Converts img to bytes object for Image.data field.
    Returns Image if data is less than max size, otherwise exits program and logs error.

        Parameters:
            img ((PIL) Image): Pillow Image object
        
        Returns:
            ((gRPC) Image): gRPC Image object for valid image
            or
            None: Exits program and logs error if image is greater than max size of 4194304 bytes
    '''
    width, height = img.size
    color = False if len(img.getbands()) == 1 else True
    data = img.tobytes()

    if len(data) <= 4194304:
        return image_pb2.Image(color=color, data=data, width=width, height=height)
    else:
        sys.exit('Error: Image greater than max size of 4194304 bytes')

def image_to_pil_image(image):
    '''
    Converts Image object into PIL Image object

    Uses Pillow Image module to construct PIL Image object from Image.data bytes object
    Sets mode ['RGB', 'RGBA', 'L'] of Image object by calculating number of channels in bytes object using image dimensions

        Parameters:
            image (gRPC Image): gRPC Image object
        
        Returns:
            (PIL Image): Pillow Image object 
    '''
    num_bands = len(image.data) / (image.width * image.height)
    mode = 'RGB' if num_bands == 3 else 'RGBA' if num_bands == 4 else 'L'
    return Image.frombytes(mode=mode, size=(image.width, image.height), data=image.data)

def get_new_pil_image_template(image_data, width, height):
    '''
    Returns empty Pillow Image object template with dimensions (width x height)

    Sets mode ['RGB', 'RGBA', 'L'] of Image object by calculating number of channels in bytes object using image dimensions
    Used to create blank image template to fill during rotation operations

        Parameters:
            image_data (bytes): Bytes object of source image, used to calculate number of bands for Image to return
            width (int): Desired width in pixels of Image to return
            height (int): Desired width in pixels of Image to return
        
        Returns:
            (Image): Blank Pillow Image template with dimensions (width x height)
    '''
    num_bands = len(image_data) / (width * height)
    mode = 'RGB' if num_bands == 3 else 'RGBA' if num_bands == 4 else 'L'
    return Image.new(mode=mode, size=(width, height))

def save_image(image, output):
    '''
    Takes in gRPC Image object and saves Image at output file path

    Calls image_to_pil_image method on image to construct Pillow Image object
    Saves this Image at output file path

        Parameters:
            image (Image): gRPC Image object of image to save
            output (str): File path with file name of output image to be saved
        Returns:
            None
    '''
    img = image_to_pil_image(image)
    img.save(output)

def get_pixels_buffer(img):
    '''
    Takes in Pillow Image object, and returns 2D array buffer storing pixel values

    Gets width and height of img from img.size
    Returns pixels array such that pixels[x][y] will be the pixel value at coordinate (x,y) in img

        Parameters:
            img (PIL Image): Pillow Image object to construct pixels buffer from
        Returns:
            pixels (2D list): 2D list representing pixel values of img
    '''
    width, height = img.size
    pixels = [ [0]*height for i in range(width)]
    for x in range(width):
        for y in range(height):
            pixels[x][y] = img.getpixel((x,y))
    return pixels

def get_pixel_neighbors(x, y, width, height):

    '''
    Returns list of tuples containing pixel coordinates representing valid neighbors of pixel (x,y)

    Calculates list of neighbors, taking into account edge and corner pixels, using image width and height

        Parameters:
            x (int): x coordinate of pixel to find neighbors of
            y (int): y coordinate of pixel to find neighbors of
            width (int): Total width in pixels of image
            height (int): Total height in pixels of image
        Returns:
            neighbors (list): List of neighbors to (x,y) as tuples in format (x_coord, y_coord)
    '''

    neighbors = []

    has_north = True if y > 0 else False
    has_south = True if y < height-1 else False
    has_west = True if x > 0 else False
    has_east = True if x < width-1 else False

    if has_north:
        neighbors.append((x, y-1))
        if has_west:
            neighbors.append((x-1, y-1))
        if has_east:
            neighbors.append((x+1, y-1))
    if has_south:
        neighbors.append((x, y+1))
        if has_west:
            neighbors.append((x-1, y+1))
        if has_east:
            neighbors.append((x+1, y+1))
    if has_west:
        neighbors.append((x-1, y))
    if has_east:
        neighbors.append((x+1, y))

    return neighbors