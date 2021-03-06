from argparse import ArgumentParser
from cam_tools import CamToolsError, label, undistort


def main():
    parser = ArgumentParser(description="Useful tools for camera calibration")
    subparsers = parser.add_subparsers(
        help="Various tools", dest="command")

    label_parser = subparsers.add_parser(
        "label", help="Easy labelling of corners")
    label_parser.add_argument(
        "-p", "--path", help="The directory of images to label", default="images")
    label_parser.add_argument(
        "-f", "--format", help="The format of the images", default="jpg")
    label_parser.add_argument(
        "-o", "--output", help="The output file to contain the corners", default="corners.csv")
    label_parser.add_argument(
        "-d", "--dimension", help="The dimension of the board", default="8x8")

    undistort_parser = subparsers.add_parser(
        "undistort", help="Undistorting images")
    undistort_parser.add_argument(
        "-p", "--path", help="The directory of images to undistort", default="images")
    undistort_parser.add_argument(
        "-f", "--format", help="The format of the images", default="jpg")
    undistort_parser.add_argument(
        "-i", "--input", help="The input file containing the corners", default="corners.csv")
    undistort_parser.add_argument(
        "-o", "--output", help="The directory for the undistorted images", default="images_undistorted")
    undistort_parser.add_argument(
        "-d", "--dimension", help="The dimension of the board", default="8x8")
    undistort_parser.add_argument(
        "-r", "--retain", help="Whether to retain pixels", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "label":
            label(args.path, args.format, args.output, args.dimension)
        elif args.command == "undistort":
            undistort(args.path, args.format, args.input,
                      args.output, args.dimension, args.retain)
    except CamToolsError as e:
        print(f'error: {e}')
        exit(1)


if __name__ == "__main__":
    main()
