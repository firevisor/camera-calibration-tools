from cam_tools.error import CamToolsError
from cam_tools.utils import parse_dimension
import cv2
import glob
import numpy as np
import pandas as pd
from pathlib import Path


def undistort(images_path, images_format, labels_path, suffix, dimension, retain_pixels):
    """Reads the labels and undistorts the images based on them.
    """

    # Extract the dimension of the board.
    dimension = parse_dimension(dimension)

    # Create the glob to read the images.
    image_paths = glob.glob(
        str(images_path / Path(f"*.{images_format}")))

    # If there are no image paths, just quit.
    if len(image_paths) == 0:
        return

    # Load the first image to obtain the width and height.
    image = cv2.imread(image_paths[0])
    if image is None:
        raise CamToolsError("failed to load initial image")

    # Read the CSV data into a `DataFrame`.
    image_points = None
    try:
        image_points = pd.read_csv(labels_path, header=None)
    except FileNotFoundError as e:
        raise CamToolsError("labels could not be found")

    # Transform the raw data frame into image points.
    image_points = extract_image_points(image_points)

    # Generate the corresponding object points.
    single_object_points = np.zeros((dimension[1]*dimension[0], 3), np.float32)
    single_object_points[:, :2] = np.mgrid[0:dimension[0],
                                           0:dimension[1]].T.reshape(-1, 2)
    object_points = [single_object_points for i in range(len(image_points))]

    # Warn if not enough points.
    if len(image_points) < 10:
        print("[WARN] Results might not be optimal with less than 10 labelled images")

    # Calculate the camera calibration.
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        object_points, image_points, image.shape[::-1][1:3], None, None)
    if not ret:
        raise CamToolsError("failed to caculate the camera calibration")

    # Turn `retain pixels` into an integer.
    if retain_pixels:
        retain_pixels = 1
    else:
        retain_pixels = 0

    # Read and undistort each image from the glob.
    for image_path in image_paths:
        image = cv2.imread(image_path)

        if image is None:
            print(f"[WARN] Failed to load image at {image_path}.")
            continue

        h, w, _ = image.shape

        # Recalculate the matrix based on `retain_pixels`.
        undist_mtx, _ = cv2.getOptimalNewCameraMatrix(
            mtx, dist, (w, h), retain_pixels, (w, h))

        # Undistort the image.
        undist_image = cv2.undistort(image, mtx, dist, None, undist_mtx)

        # Write the undistorted image.
        cv2.imwrite(str(derive_undist_image_path(
            image_path, suffix)), undist_image)


def extract_image_points(image_points):
    """Obtain a usable image points from the raw data frame.
    """

    new_image_points = []

    for single_image_points in image_points.values:
        single_image_points = np.array_split(
            single_image_points, len(single_image_points) / 2)
        single_image_points = np.array(
            [np.array([p]) for p in single_image_points])
        new_image_points.append(single_image_points)

    return np.array(new_image_points).astype('float32')


def derive_undist_image_path(image_path, suffix):
    """Adds the suffix behind the path of the undistorted image.
    """

    image_path = Path(image_path)
    return Path(image_path.parent) / Path(str(image_path.stem + suffix + image_path.suffix))