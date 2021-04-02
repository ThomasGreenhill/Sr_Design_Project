def plot(x_arr, y_arr, count=0, random=False, label=None, linestyle=None, color=None, dense=True, loose=False):
    """
    Formats and plots a single line, either in sequence or random

    :param x_arr: (array-like) data set to plot in x-dir
    :param y_arr: (array-like) data set to plot in y-dir
    :param count: (int) start with 0, count for recording the line style color number
    :param random: (bool) True for random line style & colors
    :param label: (str) label for legend
    :param linestyle: (str) line style parameter
    :param color: (str) line color parameter
    :param dense: (bool) True to enable dense dots and dashes for line style
    :param loose: (bool) True to enable loose dots and dashes for line style
    :return count: (int) the count for next function call

    History:
            Created, XT. 04.01.2021
            Debugged, XT. 04.01.2021
    """

    import matplotlib.pyplot as plt

    if linestyle is None:
        line_style_input = formatlinestyle(count, random, dense, loose)
    else:
        line_style_input = linestyle

    if color is None:
        line_color_input = formatlinecolor(count, random)
    else:

        line_color_input = color

    plt.plot(x_arr, y_arr, label=label, linestyle=line_style_input, color=line_color_input)

    return count + 1


def formatlinestyle(count, random, dense, loose):
    """
    Formats line styles in matplotlib.pyplot

    :return: a generated format of plotted line in pyplot

    History:
        Created, XT. 04.01.2021
        Debugged, XT. 04.01.2021
    """

    line_styles = {
        1: 'solid',
        2: 'dotted',
        3: 'dashed',
        4: 'dashdot',
        5: (0, (3, 5, 1, 5)),  # dash-dotted
        6: (0, (3, 5, 1, 5, 1, 5)),  # dash-dot-dotted

        21: (0, (1, 1)),  # densely dotted
        22: (0, (5, 1)),  # densely dashed
        23: (0, (3, 1, 1, 1)),  # densely dash-dotted
        24: (0, (3, 1, 1, 1, 1, 1)),  # densely dash-dot-dotted

        41: (0, (1, 10)),  # loosely dotted
        42: (0, (5, 10)),  # loosely dashed
        43: (0, (3, 10, 1, 10)),  # loosely dash-dotted
        44: (0, (3, 10, 1, 10, 1, 10))  # loosely dash-dot-dotted
    }

    line_styles.setdefault('default', [(1, 6), (21, 24), (41, 44)])

    keys = []
    for item in line_styles.keys():
        keys.append(item)

    key_ranges = [line_styles['default'][0]]

    if dense:
        key_ranges.append(line_styles['default'][1])

    if loose:
        key_ranges.append(line_styles['default'][2])

    if random:
        key = random_in_ranges(key_ranges)
    else:
        cur_count = count % len(keys)
        key = keys[cur_count]

    return line_styles[key]


def formatlinecolor(count, random):
    """
    Formats line colors in matplotlib.pyplot

    :return: a generated color of plotted line in pyplot

    History:
        Created. XT. 04.01.2021
        Debugged, XT. 04.01.2021
    """

    import random as rd

    line_colors = {
        1: 'b',  # blue
        2: 'g',  # green
        3: 'r',  # red
        4: 'c',  # cyan
        5: 'm',  # magenta
        6: 'y',  # yellow
        7: 'k'  # black
    }

    keys = []
    for item in line_colors.keys():
        keys.append(item)

    if random:
        key = rd.randint(1, 7)
    else:
        cur_count = count % len(keys)
        key = keys[cur_count]

    return line_colors[key]


def check_str(input):
    """
    Checks if the input is type <str>, raise exception if not
    :param input: input parameter, expected to be a string
    """
    if type(input) is not str:
        raise Exception('Keywords <label>, <linestyle>, <color> must be strings')


def random_in_ranges(ranges, integer=True):
    import random as rd
    import math
    out_num_arr = [0] * len(ranges)

    for ii in range(len(ranges)):
        if type(ranges[ii]) is not tuple and type(ranges[ii]) is not list:
            raise TypeError("param ranges in random_in_ranges must be a tuple or a list")

        if len(ranges[ii]) != 2:
            raise ValueError("Each range must consists of 2 values")
        LO, HI = ranges[ii]

        if LO >= HI:
            raise ValueError("Each range must in increasing order")

        if integer:
            out_num_arr[ii] = rd.randint(math.ceil(LO), math.floor(HI))
        else:
            out_num_arr[ii] = rd.uniform(LO, HI)

    key = rd.randint(0, len(out_num_arr) - 1)

    return out_num_arr[key]


if __name__ == '__main__':
    import math
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 2 * math.pi, 100)
    y = np.sin(x)

    plt_count = 0
    for ii in range(10):
        plt_count = plot(x, (1 + ii / 10) * y, plt_count, random=True, label=str(ii), dense=False, loose=True)

    plt.xlabel("x")
    plt.ylabel("sinx")
    plt.title("Sinx Function")
    plt.legend()
    plt.show()
