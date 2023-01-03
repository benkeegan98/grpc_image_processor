
# Ben Keegan - gRPC Image Rotation Service Submission

Submission requires clean install of Mac OS



### Limitations & Known Issues

Setup Script
- Setup script does not work using command `./setup`, but instead only works with command `source setup`.
    - This is because the script sets the `pyenv` version, and activates the `venv` virtual environment using `source venv/bin/activate`. With the `./setup` command, the python version is set and the virtual environment is activated inside the internal bash shell that exits when the script terminates, hence these changes don't persist in our main shell. 
    - `source setup` runs the script from our main shell, so allows these changes to persist. This was the only way I could get my setup script to work as intended.
- The setup command also requires the user to be an Administrator such that they have `sudo` permissions
    - This is required for the Homebrew installation process

### Other Considerations

Max Image Size:
 - Upon testing with a large image, I found the max image size allowed by the gRPC Service to be 4194304 bytes (4MB worth). I added a check for this before I try to create an Image object from a PIL Image.

Grayscale Single Channel vs Gray RGB:
 - I found many 'grayscale' images online that I was planning to test with, but I discovered that many of them were in fact 3 channel RGB images with the same value for R, G, and B for each pixel.
 - At first, I was torn between whether to use True or False for these Gray RGB images. I was considering running a check where I could get the sum of all the byte values for each respective channel, and if the sums of each channel were equal, the image would be a Gray RGB image.
 - I decided against overcomplicating this and stuck with the idea that Color would only equal False if the image had a single channel. This made it easier to work with, as I didn't have the added confusion that some Images with Color = False could also have more than one channel. When Color = False, I would know that each pixel held one value, and if Color = True, each pixel would either hold 3 values for RGB, or 4 values for the added Alpha channel in PNG images.

Client-side Argument Validation
 - Port Numbers:
    - I added a check so that non-positive, non-integers, and port numbers greater than 65535 would trigger a parser error. This is because 65535 is the highest TCP port number.
    - I also included this check on the server side.
 - Input and Output File Extensions:
    - I added a check so that input or output file extensions that are not '.png', '.jpg', or '.jpeg' (accounting for capitalized extensions) would trigger a parser error. Since the prompt said the client would only be tested with PNGs and JPGs, I thought that this check would be worthwhile, since it prevents against reading an input image, or saving an output image, with an invalid extension, or without any extension at all.
 - Rotate and Mean Flags
    - I added a check so that either the --rotate or --mean (or both) flags must be present. This is because it does not make sense to run the program without either of these options. Omitting both with trigger a parser error.

Test Cases
 - Tests reside in the `src/tests` package. The test runner can be run from this package with `python tests.py`. I also set this automated test suite to run as part of the `./build` command, ensuring this was the last build step.
 - I decided to break it down into unit tests for the `image_utils` methods (found in `src/tests/image_utils_tests`) , and tests for the gRPC implementations (found in `src/tests/grpc_tests`). The `grpc_tests` include test cases for the ImageServiceServicer independent of the client (found in `test_image_server.py`), and test cases for the client methods in how they call the server endpoints (found in `test_image_client.py`).
 - I included a `test_images` folder including sample images that I use to run test cases against.

