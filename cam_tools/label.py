from cam_tools.error import CamToolsError
import cv2
import glob
from pathlib import Path

WINDOW_HEIGHT = 480


def label(images_path, images_format, output_path, dimension):
    """Easy labelling of corners on the images in the directory.

    Displays the images in the directory one at a time and writes the labelling
    results into a CSV file at the given output path.
    """

    # Extract the dimension of the board.
    dimension = parse_dimension(dimension)

    # Create the glob to read the images.
    image_paths = glob.glob(
        str(Path(images_path) / Path(f"*.{images_format}")))

    # Read and display each image from the glob, and collect the labelling.
    for image_path in image_paths:
        image = cv2.imread(image_path)

        # Temporarily resize the image, so the window doesn't appear enormous.
        height, width, _ = image.shape
        scale = height / 480
        small_image = cv2.resize(
            image, (int(width / scale), int(height / scale)))

        if image is None:
            print(f"[WARN] Failed to load image at {image_path}.")
            continue

        display_and_label(small_image, dimension)

    raise NotImplementedError()


def display_and_label(image, dimension):
    """Displays the given image in a window and collects the labelling.
    """

    cv2.imshow("Label", image)
    cv2.waitKey(0)


def parse_dimension(dimension):
    """Parse the given dimension (e.g. 8x8) and returns a tuple (e.g. `(8, 8)`).
    """

    dimension = [comp.strip() for comp in dimension.split("x")]

    if len(dimension) != 2:
        raise CamToolsError("invalid dimension: expected exactly 2 components")

    try:
        dimension = list(map(int, dimension))
    except ValueError as e:
        raise CamToolsError("invalid dimension: expected integer components")

    return (dimension[0], dimension[1])
