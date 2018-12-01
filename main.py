from argparse import ArgumentParser
from cam_tools import CamToolsError, label


def main():
    parser = ArgumentParser(description="Useful tools for camera calibration")
    subparsers = parser.add_subparsers(
        help="Various tools", dest="command")

    label_parser = subparsers.add_parser(
        "label", help="Corner labelling for effective calibration")
    label_parser.add_argument(
        "-p", "--path", help="The directory of images to label", default="data")

    args = parser.parse_args()

    try:
        if args.command == "label":
            label(args.path)
    except CamToolsError as e:
        print(f'error: {e}')
        exit(1)


if __name__ == "__main__":
    main()
