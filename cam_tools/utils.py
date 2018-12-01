from cam_tools.error import CamToolsError


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
