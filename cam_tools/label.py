from cam_tools.error import CamToolsError
from cam_tools.utils import parse_dimension
import cv2
import glob
import numpy as np
import pandas as pd
from pathlib import Path

WINDOW_NAME = "Label"
WINDOW_HEIGHT = 800
CIRCLE_RADIUS = 5


def label(images_path, images_format, output_path, dimension):
    """Provides easy labelling of corners on the images in the directory through
    an OpenCV GUI.

    Displays the images from the directory one at a time. Click the corners from
    left-to-right and top-to-bottom, and then press any key to go to the next
    image.

    When the image is clicked wrongly, press "backspace" to go back one corner.
    If an image is not fully labelled before a key is pressed, the image will be
    ignored.

    Once completed, the corners will be written into a CSV file at the given
    output path, which can then be used to undistort the image.
    """

    cv2.namedWindow(WINDOW_NAME)

    # Convert the string paths into `Path`s.
    images_path = Path(images_path)
    output_path = Path(output_path)

    # Extract the dimension of the board.
    dimension = parse_dimension(dimension)

    # Create the glob to read the images.
    image_paths = glob.glob(
        str(images_path / Path(f"*.{images_format}")))

    # Store the image points/corners here, to write into the CSV file later.
    image_points = []

    # Read and display each image from the glob, and collect the corners.
    for image_path in image_paths:
        image = cv2.imread(image_path)

        # Ignore images that fail to load.
        if image is None:
            print(f"[WARN] Failed to load image at {image_path}.")
            continue

        # Temporarily resize the image, so the window doesn't appear enormous.
        height, width, _ = image.shape
        scale = height / WINDOW_HEIGHT
        small_image = cv2.resize(
            image, (int(width / scale), int(height / scale)))

        # Collect the corners.
        corners = label_image(small_image, dimension)

        # Scale the corners back up (the image was scaled down above).
        corners = [[corner[0] * scale, corner[1] * scale]
                   for corner in corners]
        corners = np.array(corners).flatten()
        image_points.append(corners)

    # Write the corners into a CSV.
    try:
        image_points = pd.DataFrame(np.array(image_points))
        image_points.to_csv(str(output_path),
                            header=None, index=None)
    except FileNotFoundError as e:
        raise CamToolsError("could not write to output file")


def label_image(image, dimension):
    """Displays the given image in a window for labelling and collects the
    resulting corners.

    Each time a click occurs, the click is saved and a circle is drawn onto the
    image (the previous image is saved) for feedback. The new image is then
    shown on the window.

    Each time "backspace" is pressed, the current image and click is discarded
    and the previous image is shown on the window.
    """

    # Stores the current state of the labelling.
    corners = []
    images = [image]

    # Display the image and collect clicks.
    while True:
        cv2.setMouseCallback(WINDOW_NAME, lambda event, x, y, flags,
                             param: handle_click(corners, images, event, x, y))
        cv2.imshow(WINDOW_NAME, images[len(images) - 1])
        cv2.waitKey(0)

        # Check whether there are enough corners.
        if len(corners) == dimension[0] * dimension[1]:
            break

    return corners


def handle_click(corners, images, event, x, y):
    """Handles a single click.

    Draws a circle onto the current image, and saves the new image and the
    corner into the given state (e.g. corners and images). Then, displays the
    new image.
    """

    # Ignore non-click events.
    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # Get the current image.
    cur_image = images[len(images) - 1]

    # Draw a circle onto the current image.
    new_image = cv2.circle(cur_image, (x, y), CIRCLE_RADIUS, (0, 255, 0))

    # Append the new corners and image.
    corners.append([x, y])
    images.append(new_image)

    # Display the new image.
    cv2.imshow(WINDOW_NAME, new_image)
