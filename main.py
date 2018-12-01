from argparse import ArgumentParser
from cam_tools import CamToolsError, label, undistort


def main():
    parser = ArgumentParser(description="Useful tools for camera calibration")
    subparsers = parser.add_subparsers(
        help="Various tools", dest="command")

    label_parser = subparsers.add_parser(
        "label", help="Easy corner labelling")
    label_parser.add_argument(
        "-p", "--path", help="The directory of images to label", default="images")
    label_parser.add_argument(
        "-f", "--format", help="The format of the images", default="jpg")
    label_parser.add_argument(
        "-o", "--output", help="The output file (CSV format)", default="labels.csv")
    label_parser.add_argument(
        "-d", "--dimension", help="The dimension of the board", default="8x8")

    undistort_parser = subparsers.add_parser(
        "undistort", help="Undistorting images")
    undistort_parser.add_argument(
        "-p", "--path", help="The directory of images to undistort", default="images")
    undistort_parser.add_argument(
        "-f", "--format", help="The format of the images", default="jpg")
    undistort_parser.add_argument(
        "-l", "--labels", help="The file containing the labels", default="labels.csv")
    undistort_parser.add_argument(
        "-s", "--suffix", help="The suffix for the undistorted images", default="_undistorted")
    undistort_parser.add_argument(
        "-d", "--dimension", help="The dimension of the board", default="8x8")
    undistort_parser.add_argument(
        "-r", "--retain", help="Whether to retain pixels", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "label":
            label(args.path, args.format, args.output, args.dimension)
        elif args.command == "undistort":
            undistort(args.path, args.format, args.labels,
                      args.suffix, args.dimension, args.retain)
    except CamToolsError as e:
        print(f'error: {e}')
        exit(1)


if __name__ == "__main__":
    main()
