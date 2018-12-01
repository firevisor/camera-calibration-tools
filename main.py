from argparse import ArgumentParser
from cam_tools import CamToolsError, label


def main():
    parser = ArgumentParser(description="Useful tools for camera calibration")
    subparsers = parser.add_subparsers(
        help="Various tools", dest="command")

    label_parser = subparsers.add_parser(
        "label", help="Easy corner labelling")
    label_parser.add_argument(
        "-p", "--path", help="The directory of images to label", default="data")
    label_parser.add_argument(
        "-f", "--format", help="The format of the images", default="jpg")
    label_parser.add_argument(
        "-o", "--output", help="The output file (CSV format)", default="labels.csv")
    label_parser.add_argument(
        "-d", "--dimension", help="The dimension of the board", default="8x8")

    args = parser.parse_args()

    try:
        if args.command == "label":
            label(args.path, args.format, args.output, args.dimension)
    except CamToolsError as e:
        print(f'error: {e}')
        exit(1)


if __name__ == "__main__":
    main()
