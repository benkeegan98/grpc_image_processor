import argparse
import image_pb2

def get_server_args_parser():
    '''
    Returns argparse argument parser for server.py

    Sets valid arguments for server.py.
    Ensures that --host and --port arguments are both required

        Parameters:
            None
        Returns:
            parser (argparse.ArgumentParser): Argument parser containing arguments for server.py
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, action='store', help='Host name')
    parser.add_argument('--port', required=True, action='store', help='Port number')
    return parser

def get_client_args_parser():
    '''
    Returns argparse argument parser for client.py

    Sets valid arguments for client.py.
    Ensures that --host, --port, --input, and --output arguments are all required.
    Provides list of enum choices for --rotate argument.
    Ensures that --mean argument value is set to True when flag is present, False when flag not present

        Parameters:
            None
        Returns:
            parser (argparse.ArgumentParser): Argument parser containing arguments for client.py
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, action='store', help='Host name')
    parser.add_argument('--port', required=True, action='store', help='Port number')
    parser.add_argument('--input', required=True, action='store', help='Input image file path')
    parser.add_argument('--output', required=True, action='store', help='Output image file path')
    parser.add_argument('--rotate', action='store', choices=image_pb2.ImageRotateRequest.Rotation.keys(), help='Rotation enum input')
    parser.add_argument('--mean', action='store_true', help='Apply mean filter')
    return parser

