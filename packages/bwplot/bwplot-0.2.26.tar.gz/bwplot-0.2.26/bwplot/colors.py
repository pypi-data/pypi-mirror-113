

def cbox(i, gray=False, spectrum="alternate", reverse=False, as255=False, alpha=None, **kwargs):
    """
    Access a modular list of colors for plotting.
    Defines colours using rgb.

    :param i: (int), index to access color
    :param gray: (bool), if true then color is return as grayscale value
    :param spectrum: (str), choice of spectrum to use
    :param reverse: (bool), reverses the color order
    :param kwargs:
    :return:
    """

    CD = {}
    CD['dark blue'] = (0.0, 0.0, 0.55)  # 0
    CD['greenish blue'] = (0.12, .8, .8)  # 10
    CD['dark green'] = (0.15, 0.35, 0.0)  # 1
    CD['yellow'] = (1.0, 1.0, 0.0)  # 6
    CD['orangish yellow'] = (1.0, 0.9, 0.1)  # 6
    CD['dark red'] = (0.73, 0.0, 0.0)  # 2
    CD['dark purple'] = (0.8, 0.0, 0.8)  # 3
    CD['light green'] = (0.49, 0.64, 0.0)  # 4
    CD['orange'] = (1.0, 0.5, 0.0)  # 5
    CD['light blue'] = (0.5, 0.85, 1.0)  # 6
    CD['pink'] = (1.0, 0.8, 0.8)  # 7
    CD['brown'] = (0.5, 0.3, 0.0)  # 8
    CD['red'] = (0.9, 0.0, 0.0)  # 9

    CD['bluey purple'] = (0.8, 0.85, 1.0)  # 12

    CD['dark gray'] = (0.25, 0.25, 0.25)  #
    CD['mid gray'] = (0.5, 0.5, 0.5)  #
    CD['light gray'] = (0.75, 0.75, 0.75)  #
    CD['dark grey'] = (0.25, 0.25, 0.25)  #
    CD['mid grey'] = (0.5, 0.5, 0.5)  #
    CD['light grey'] = (0.75, 0.75, 0.75)  #
    CD['black5'] = (0.05, 0.05, 0.05)  #
    CD['black'] = (0.0, 0.0, 0.0)  #
    CD['white'] = (1.0, 1.0, 1.0)  #

    if isinstance(i, int):
        i = i
    elif isinstance(i, float):
        i = int(i)
    elif isinstance(i, str):
        dat = CD[i]
        return dat
    if spectrum == "alternate":
        order = ['dark blue', 'orange', 'light blue', 'dark purple', 'dark green',
                 'bluey purple', 'dark red', 'light green', 'pink', 'brown',
                 'red', 'yellow', 'greenish blue', 'dark gray',
                 'mid gray', 'light gray']
    elif spectrum == "lighten":
        order = ['dark blue', 'dark green', 'dark red', 'brown',
                 'light green', 'orange', 'light blue', 'pink', 'dark purple',
                 'red', 'greenish blue', 'bluey purple', 'yellow',
                 'dark gray', 'mid gray', 'light gray']
    elif spectrum == 'dots':
        order = ['dark blue', 'yellow', 'light blue', 'dark purple', 'dark green', 'orange',
                 'bluey purple', 'dark red', 'light green', 'pink', 'brown',
                 'red', 'greenish blue', 'dark gray',
                 'mid gray', 'light gray']
    elif spectrum == "traffic":
        order = ['dark green', 'orange', 'red']
    else:  # warnings
        order = ['light green', 'orangish yellow', 'orange', 'red', 'black', 'dark gray']

    index = i % len(order)
    if reverse:
        index = len(order) - index - 1
    rgb = CD[order[index]]

    gray_value = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]  # calculate the gray scale value

    if gray:
        return gray_value, gray_value, gray_value
    if as255:
        rgb = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
    if alpha:
        rgb = list(rgb)
        rgb.append(alpha)
    return rgb


def spectra(i, **kwargs):
    """
    Define colours by number.
    Can be plotted either in order of gray scale or in the 'best' order for
    having a strong gray contrast for only three or four lines
    :param i: the index to access a colour
    """
    ordered = kwargs.get('ordered', False)
    options = kwargs.get('options', 'best')
    gray = kwargs.get('gray', False)
    CD = {}
    CD['dark blue'] = (1.0, 0.0, 0.55)  # 0
    CD['dark green'] = (0.15, 0.35, 0.0)  # 1
    CD['dark red'] = (0.73, 0.0, 0.0)  # 2
    CD['dark purple'] = (0.8, 0.0, 0.8)  # 3
    CD['light green'] = (0.49, 0.64, 0.0)  # 4
    CD['orange'] = (1.0, 0.5, 0.0)  # 5
    CD['light blue'] = (0.5, 0.85, 1.0)  # 6
    CD['pink'] = (1.0, 0.8, 0.8)  # 7
    CD['brown'] = (0.5, 0.3, 0.0)  # 8
    CD['red'] = (0.9, 0.0, 0.0)  # 9
    CD['greenish blue'] = (0.12, .8, .8)  # 10
    CD['bluey purple'] = (0.8, 0.85, 1.0)  # 12
    CD['yellow'] = (1.0, 1.0, 0.0)  # 6
    CD['dark gray'] = (0.25, 0.25, 0.25)  #
    CD['mid gray'] = (0.5, 0.5, 0.5)  #
    CD['light gray'] = (0.75, 0.75, 0.75)  #
    CD['black5'] = (0.05, 0.05, 0.05)  #
    CD['black'] = (0.0, 0.0, 0.0)  #
    CD['white'] = (1.0, 1.0, 1.0)  #

    if isinstance(i, int):
        i = i
    elif isinstance(i, float):
        i = int(i)
    elif isinstance(i, str):
        dat = CD[i]
        return dat

    DtoL = ['dark blue', 'dark green', 'dark red', 'brown',
            'light green', 'orange', 'light blue', 'pink', 'dark purple',
            'red', 'greenish blue', 'bluey purple', 'yellow',
            'dark gray', 'mid gray', 'light gray']
    Best = ['dark blue', 'orange', 'light blue', 'dark purple', 'dark green',
            'bluey purple', 'dark red', 'light green', 'pink', 'brown',
            'red', 'yellow', 'greenish blue', 'dark gray',
            'mid gray', 'light gray']
    Dots = ['dark blue', 'yellow', 'light blue', 'dark purple', 'dark green', 'orange',
            'bluey purple', 'dark red', 'light green', 'pink', 'brown',
            'red', 'greenish blue', 'dark gray',
            'mid gray', 'light gray']
    # ll = [0, 5, 2, 4, 1, 6, 3, 7, 8, 11, 9, 12, 10, 13, 14, 15]  # change 11 w 5

    ind = i % len(Best)
    dat = CD[Best[ind]]
    col = Best[ind]
    if ordered:  # if ordered is true then the colours are accessed from darkest to lightest
        ind = i % len(DtoL)
        dat = CD[DtoL[ind]]
        col = DtoL[ind]
    if options == "dots":
        ind = i % len(Dots)
        dat = CD[Dots[ind]]
        col = Dots[ind]
    if options == "ordered":
        ind = i % len(DtoL)
        dat = CD[DtoL[ind]]
        col = DtoL[ind]

    gray_value = 0.299 * dat[0] + 0.587 * dat[1] + 0.114 * dat[2]  # calculate the gray scale value

    if gray:
        return gray_value, gray_value, gray_value

    return dat


#
# def assessClassicColours():
#     cl = ['b', 'g', 'r', 'm', 'y', 'k', 'ivory', 'orange']
#     cc = ColorConverter()  # ColorConverter from matplotlib
#     for ss in cl:
#         print(ss)
#         col = cc.to_rgb(ss)
#         print(col)
#         gray = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
#         print(gray)
#
#
# def plotter():
#     cs = 16
#     for j in range(cs):
#         a = np.arange(0, 10, 1)
#         b = 0.1 * np.ones(10)
#         # plt.plot(a, b + j, c=cbox('red', ordered=True), lw=30)
#         # plt.plot(a, b + j, c=cbox(j, ordered=True), lw=30)
#         plt.plot(a, b + j, c=cbox(j, ordered=False), lw=30)
#     plt.show()
#
#
# def checkGreys():
#     cs = 16
#     for j in range(cs):
#         a = np.arange(0, 5, 1)
#         b = 0.1 * np.ones(5)
#         # plt.plot(a, b + j, c=cbox('red', ordered=True), lw=30)
#         # plt.plot(a, b + j, c=cbox(j, ordered=True), lw=30)
#         col = cbox(j, ordered=False)
#         gray = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
#         plt.plot(a, b + j, c=col, lw=30)
#         d = np.arange(4, 9, 1)
#         print('gray value: ', gray)
#         plt.plot(d, b + j, c=(gray, gray, gray), lw=30)
#     plt.show()

def red_to_yellow(i, gray=False, reverse=False, as255=False, alpha=None):
    rgbs = [[167, 44, 24],
            [175, 65, 33],
            [186, 90, 44],
            [195, 114, 56],
            [206, 141, 69],
            [217, 168, 83],
            [230, 197, 98],
            [242, 224, 112],
            [253, 250, 125]]
    ind = i % len(rgbs)
    if reverse:
        ind = len(rgbs) - ind - 1
    rgb = rgbs[ind]

    gray_value = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255  # calculate the gray scale value

    if gray:
        return gray_value, gray_value, gray_value
    if not as255:
        rgb = [float(rgb[0]) / 255, float(rgb[1]) / 255, float(rgb[2]) / 255]
    if alpha:
        rgb = list(rgb)
        rgb.append(alpha)
    return rgb


def get_len_red_to_yellow():
    return 9


RED2YELLOW2BLUE_STR = 'red2yellow2blue'
RED2WHITE2BLUE_STR = 'red2white2blue'
PURPLE2GREEN_STR = 'purple2green'
RED2YELLOWWHITE = 'red2yellowwhite'

COLOR_SCHEMES = [RED2YELLOW2BLUE_STR, RED2WHITE2BLUE_STR, PURPLE2GREEN_STR, RED2YELLOWWHITE]


def get_colors(scheme):
    if scheme == PURPLE2GREEN_STR:
        rgbs = [
            [73, 23, 118],  # 0
            [100, 32, 111],
            [130, 39, 108],
            [153, 51, 99],  # 3
            [173, 68, 74],  # 4
                [184, 87, 62],  # 5
                [195, 105, 54],  # 6
                [198, 126, 56],  # 7
                [206, 143, 64],  # 8
                [209, 163, 71],
                [207, 184, 90],
                [196, 207, 120],
                [183, 234, 134],
                [181, 255, 148],
                ]
    elif scheme == 'purple2yellow':
        rgbs = [
            [73, 15, 96],
            [70, 44, 159],
            [113, 62, 146],
            [173, 74, 126],
            [195, 102, 120],
            [234, 129, 87],
            [250, 165, 62],
            [250, 202, 72],
            [251, 238, 95],
        ]
    elif scheme == 'red2yellow':
        rgbs = [[167, 44, 24],
                [175, 65, 33],
                [186, 90, 44],
                [195, 114, 56],
                [206, 141, 69],
                [217, 168, 83],
                [230, 197, 98],
                [242, 224, 112],
                [253, 250, 125],
                ]
    elif scheme == 'red2yellowwhite':
        rgbs = [[167, 44, 24],  # 0
                [175, 65, 33],  # 1
                [186, 90, 44],  # 2
                [195, 114, 56],  # 3
                [206, 141, 69],  # 4
                [217, 168, 83],  # 5
                [230, 197, 98],  # 6
                [242, 224, 112],  # 7
                [253, 250, 125],  # 8
                [250, 250, 240],  # 9
                ]
    elif scheme == 'red2yellow2green':
        rgbs = [[167, 44, 24],  # 9
                [175, 65, 33],  # 8
                [186, 90, 44],  # 7
                [195, 114, 56],  # 6
                [206, 141, 69],  # 5
                [217, 168, 83],  # 4
                [230, 197, 98],  # 3
                [242, 224, 112],  # 2
                [253, 250, 125],  # 1
                [215, 245, 130],
                [185, 240, 134],
                [157, 235, 138],
                [130, 230, 142],
                ]
    elif scheme == RED2YELLOW2BLUE_STR:
        rgbs = [[167, 44, 24],  # 0
                [175, 65, 33],  # 1
                [186, 90, 44],  # 2
                [195, 114, 56],  # 3
                [206, 141, 69],  # 4
                [217, 168, 83],  # 5
                [230, 197, 98],  # 6
                [242, 224, 112],  # 7
                [253, 240, 125],  # 8
                [250, 245, 200],  # centre
                [233, 254, 210],  # centre
                [215, 243, 140],  # 8
                [185, 236, 155],  # 7
                [157, 229, 170],  # 6
                [133, 218, 185],  # 5
                [112, 206, 200],  # 4
                [93, 193, 215],  # 3
                [74, 175, 227],  # 2
                [56, 150, 241],  # 1
                [40, 120, 253],  # 0
                ]
    elif scheme == RED2WHITE2BLUE_STR:
        rgbs = [[167, 44, 24],  # 0
                [175, 65, 33],  # 1
                [186, 90, 44],  # 2
                [195, 114, 56],  # 3
                [206, 141, 69],  # 4
                [217, 168, 83],  # 5
                [230, 197, 98],  # 6
                [242, 224, 112],  # 7
                [253, 240, 125],  # 8
                [250, 250, 250],  # centre
                [250, 250, 250],  # centre
                [215, 243, 140],  # 8
                [185, 236, 155],  # 7
                [157, 229, 170],  # 6
                [133, 218, 185],  # 5
                [112, 206, 200],  # 4
                [93, 193, 215],  # 3
                [74, 175, 227],  # 2
                [56, 150, 241],  # 1
                [40, 120, 253],  # 0
                ]
    else:
        raise ValueError("scheme must be 'purple2green', 'purple2yellow'")
    return rgbs


def calc_cmyk_from_rgb(rgb, as255=False):
    try:
        import numpy as np
        rgb_c = np.array(rgb)
        if as255:
            rgb_c = rgb_c / 255
        k = 1 - np.max(rgb_c, axis=0)
        c = (1 - rgb_c[0] - k) / (1 - k)
        m = (1 - rgb_c[1] - k) / (1 - k)
        y = (1 - rgb_c[2] - k) / (1 - k)
        if as255:
            return np.array([c, m, y, k]) * 100
        return np.array([c, m, y, k])
    except ModuleNotFoundError:
        rc = rgb[0]
        gc = rgb[1]
        bc = rgb[2]
        if as255:
            rc /= 255
            gc /= 255
            bc /= 255
        k = 1 - max([rc, gc, bc])
        c = (1 - rc - k) / (1 - k)
        m = (1 - gc - k) / (1 - k)
        y = (1 - bc - k) / (1 - k)
        if as255:
            return c * 100, m * 100, y * 100, k * 100
        return c, m, y, k


def calc_rgb_from_cmyk(cmyk, as255=False):
    try:
        import numpy as np
        cmyk_c = np.array(cmyk)
        if as255:
            cmyk_c = cmyk_c / 100
        r = (1 - cmyk_c[0]) * (1 - cmyk_c[3])
        g = (1 - cmyk_c[1]) * (1 - cmyk_c[3])
        b = (1 - cmyk_c[2]) * (1 - cmyk_c[3])
        if as255:
            return np.array([r, g, b]) * 255
        return np.array([r, g, b])
    except ModuleNotFoundError:
        cc = cmyk[0]
        mc = cmyk[1]
        yc = cmyk[2]
        kc = cmyk[3]
        if as255:
            cc /= 100
            mc /= 100
            yc /= 100
            kc /= 100
        r = (1 - cc) * (1 - kc)
        g = (1 - mc) * (1 - kc)
        b = (1 - kc) * (1 - kc)
        if as255:
            return r * 255, g * 255, b * 255
        return r, g, b

def color_by_scheme(scheme, i, gray=False, reverse=False, as255=False, alpha=None):

    rgbs = get_colors(scheme)
    ind = i % len(rgbs)
    if reverse:
        ind = len(rgbs) - ind - 1
    rgb = rgbs[ind]

    if gray:
        gray_value = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255  # calculate the gray scale value
        return gray_value, gray_value, gray_value
    if not as255:
        rgb = [float(rgb[0]) / 255, float(rgb[1]) / 255, float(rgb[2]) / 255]
    if alpha:
        rgb = list(rgb)
        rgb.append(alpha)
    return rgb


def get_len_purple_to_green():
    return 12


def show_cbox_in_gray():
    import numpy as np
    import matplotlib.pyplot as plt
    cs = 16
    for j in range(cs):
        a = np.arange(0, 5, 1)
        b = 0.1 * np.ones(5)
        # plt.plot(a, b + j, c=cbox('red', ordered=True), lw=30)
        # plt.plot(a, b + j, c=cbox(j, ordered=True), lw=30)
        col = cbox(j, ordered=False)
        gray = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
        plt.plot(a, b + j, c=col, lw=30)
        d = np.arange(4, 9, 1)
        print('gray value: ', gray)
        plt.plot(d, b + j, c=(gray, gray, gray), lw=30)

    plt.show()

def show_in_gray(scheme):
    import numpy as np
    import matplotlib.pyplot as plt
    rgbs = get_colors(scheme)
    cs = 16
    gs = []
    for j in range(len(rgbs) + 1):
        a = np.arange(0, 5, 1)
        b = 0.1 * np.ones(5)
        # plt.plot(a, b + j, c=cbox('red', ordered=True), lw=30)
        # plt.plot(a, b + j, c=cbox(j, ordered=True), lw=30)
        col = color_by_scheme(scheme, j)
        gray = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
        plt.plot(a, b + j, c=col, lw=30)
        d = np.arange(4, 9, 1)
        print('gray value: ', gray)
        plt.plot(d, b + j, c=(gray, gray, gray), lw=30)
        plt.plot(gray * 5, j, 'o')
        gs.append(gray)
    plt.plot([gs[0] * 5, gs[-2] * 5], [0, len(rgbs) - 1])
    plt.show()


def color_by_interp(scheme, val, gray=False, reverse=False, as255=False, alpha=None):
    import numpy as np
    rgbs = np.array(get_colors(scheme))
    if reverse:
        rgbs = rgbs[::-1]
    xs = np.linspace(0, 1, len(rgbs))
    r = np.interp(val, xs, rgbs[:, 0])
    g = np.interp(val, xs, rgbs[:, 1])
    b = np.interp(val, xs, rgbs[:, 2])
    rgb = [r, g, b]
    if gray:
        gray_value = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255  # calculate the gray scale value
        return gray_value, gray_value, gray_value
    if not as255:
        rgb = [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255]
    else:
        rgb = np.array(rgb, dtype=int)
    if alpha:
        rgb = list(rgb)
        rgb.append(alpha)
    return rgb

def color_by_index(scheme, ind, gray=False, reverse=False, as255=False, alpha=None):
    import numpy as np
    rgbs = np.array(get_colors(scheme))
    if reverse:
        rgbs = rgbs[::-1]

    rgb = rgbs[ind]
    if gray:
        gray_value = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255  # calculate the gray scale value
        return gray_value, gray_value, gray_value
    if not as255:
        rgb = [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255]
    else:
        rgb = np.array(rgb, dtype=int)
    if alpha:
        rgb = list(rgb)
        rgb.append(alpha)
    return rgb


def show_interp_gray_val(scheme):
    import numpy as np
    import matplotlib.pyplot as plt
    xs = np.linspace(0, 1, 100)
    rrr = get_colors(scheme)
    cols = np.array(get_colors(scheme)) / 255

    grays = color_by_interp(scheme, xs, gray=True)

    rgbs = color_by_interp(scheme, xs)
    cmyks = calc_cmyk_from_rgb(rgbs)
    rgbs_d = calc_rgb_from_cmyk(cmyks)
    xs *= len(rrr)
    bf, sps = plt.subplots()
    plt.plot(xs, grays[0], c=(0.2, 0.2, 0.2))
    # plt.plot(xs[1:], np.diff(grays[0]) * 100, c=(0.3, 0.3, 0.3), ls='--')
    plt.plot(xs, rgbs[0], c='r')
    plt.plot(xs, rgbs[1], c='g')
    plt.plot(xs, rgbs[2], c='b')
    plt.plot(xs, rgbs_d[0], 'r--')
    plt.plot(xs, rgbs_d[1], 'g--')
    plt.plot(xs, rgbs_d[2], 'b--')
    plt.plot(xs, cmyks[0], c='c')
    plt.plot(xs, cmyks[1], c='m')
    plt.plot(xs, cmyks[2], c='y')
    plt.plot(xs, cmyks[3], c='k')
    xs1 = list(xs) + [xs[-1] + 1]
    rgbs = np.array(rgbs)
    for i in range(len(xs) - 1):
        plt.fill_between([xs1[i], xs1[i+1]], [1, 1], [1.2, 1.2], color=rgbs[:, i])
    xns = np.arange(len(cols) + 1)
    for i in range(len(cols)):
        print(cols[i])
        plt.fill_between([xns[i], xns[i+1]], [1.2, 1.2], [1.4, 1.4], color=cols[i])
    sps.xaxis.grid(True)
    plt.show()



if __name__ == '__main__':
    # show_in_gray('purple2green')
    show_interp_gray_val('red2yellow2blue')
    # show_interp_gray_val('red2yellowwhite')
    # cmyk = calc_cmyk_from_rgb((59, 132, 216), as255=True)
    # rgb = calc_rgb_from_cmyk(cmyk, as255=True)
    # print(rgb)
    # show_in_gray('purple2yellow')
    # for i in range(10):
    #     print(purple_to_green(i, True))