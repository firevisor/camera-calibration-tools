from cam_tools.error import CamToolsError
import cv2
import glob
from pathlib import Path

WINDOW_NAME = "Label"
WINDOW_HEIGHT = 480


def label(images_path, images_format, output_path, dimension):
    """Easy labelling of corners on the images in the directory.

    Displays the images in the directory one at a time and writes the labelling
    results into a CSV file at the given output path.
    """

    cv2.namedWindow(WINDOW_NAME)

    # Extract the dimension of the board.
    dimension = parse_dimension(dimension)

    # Create the glob to read the images.
    image_paths = glob.glob(
        str(Path(images_path) / Path(f"*.{images_format}")))

    # Store the image points/corners here, to write into the CSV file later.
    image_points = []

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

        # Collect the labelling.
        corners = display_and_label(small_image, dimension)

        if corners is None:
            continue
        else:
            # Scale the corners back up.
            corners = [[corner[0] * scale, corner[1] * scale]
                       for corner in corners]
            image_points.append(corners)

    raise NotImplementedError()


def display_and_label(image, dimension):
    """Displays the given image in a window and collects the labelling.
    """

    # Stores the click events for further processing.
    clicks = []

    # Display the image and collect clicks.
    cv2.setMouseCallback(WINDOW_NAME, lambda event, x, y,
                         flags, param: clicks.append((event, x, y, flags, param)))
    cv2.imshow(WINDOW_NAME, image)
    cv2.waitKey(0)

    # Keep only the left click events.
    clicks = list(
        filter(lambda click: click[0] == cv2.EVENT_LBUTTONDOWN, clicks))

    # Check whether the clicks are valid.
    if len(clicks) != dimension[0] * dimension[1]:
        print("[WARN] Number of clicks does not match dimensions, ignoring this image")
        return None

    # Change all the events to points.
    corners = []
    for click in clicks:
        _, x, y, _, _ = click
        corners.append([x, y])

    return corners


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
