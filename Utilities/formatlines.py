def formatlinestyle(dense=True, loose=False):
    """
    Formats line styles in matplotlib.pyplot

    :return: a generated format of plotted line in pyplot

    History:
        Created. XT. 04.01.2021
    """

    print('dense: ' + str(dense))
    print('loose: ' + str(loose))

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

    line_styles.setdefault('default', 'Error in dictionary line_style in formatlinestyle()')
    key_ranges = [(1, 6)]
    if dense:
        key_ranges.append((21, 24))
    if loose:
        key_ranges.append((41, 44))
    key = random_in_ranges(key_ranges)

    return line_styles[key]


def formatlinecolor():
    """
    Formats line colors in matplotlib.pyplot

    :return: a generated color of plotted line in pyplot

    History:
        Created. XT. 04.01.2021
    """

    import random as rd

    line_color = {
        1: 'b',  # blue
        2: 'g',  # green
        3: 'r',  # red
        4: 'c',  # cyan
        5: 'm',  # magenta
        6: 'y',  # yellow
        7: 'k'  # black
    }

    line_color.setdefault('default', 'Error in dictionary line_color in formatlinecolor()')
    key = rd.randint(1, 7)

    return line_color[key]


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

    plt.plot(x, y, linestyle=formatlinestyle(), color=formatlinecolor())
    for ii in range(10):
        plt.plot(x, (1 + ii / 10) * y, linestyle=formatlinestyle(), color=formatlinecolor())
    plt.xlabel("x")
    plt.ylabel("sinx")
    plt.title("Sinx Function")
    plt.show()
