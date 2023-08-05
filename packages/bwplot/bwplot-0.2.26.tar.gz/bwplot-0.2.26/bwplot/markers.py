marker_styles = [
    "x",
    "o",
    "v",
    "*",
    "^",
    "s",
    "P",  # bold plus
    "<",
    ">",
    "D",
    "1",  # y-symbol
    "2",  # upside-down y
    "p",
r'$\clubsuit$',
r'$\spadesuit$',
r'$\bigodot$', 
    r'$\bigotimes$', 
    r'$\bigoplus$',
r'$\oslash$'
]


def mkbox(i):
    """
    Cycles through marker styles based on index

    :param i: int, index for marker
    :return:
    """
    indy = i % len(marker_styles)
    return marker_styles[indy]
