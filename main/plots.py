# ============================================== #
# Plots functions                                #
# Author : Quentin Prieels                       #
# Date : April 2021                              #
# Version 1.0                                    #
# ============================================== #

# Package
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

# From project files
from HelpFunctions import warningText


def onclick(event):
    x1, y1 = event.xdata, event.ydata
    print(x1, y1)


def plot_signals(x, signals, signals_names, x_label="", y_label="", title="", saving=False):
    """
    Plot the different signals of the signals list as function of x
    :param x: List of dimension n containing the abscissas at which the signals are evaluated
    :type x: numpy.ndarray
    :param signals: List m by n of m signals evaluate in n points (the points of x list)
    :type signals: list of numpy.ndarray
    :param signals_names: List of dimension m containing all the names of the signals
    :type signals_names: list of str
    :param x_label: Name of horizontal axis
    :type x_label: str
    :param y_label: Name of the vertical axis
    :type y_label: str
    :param title: Title of the plot figure
    :type title: str
    :param saving: To know of the plot will be save or not
    :type saving: bool
    :return: Show a plot of all the signals into a unique graph
    """
    # Size of parameters
    n = len(x)
    m = len(signals)

    fig, ax = plt.subplots()

    # Errors
    if len(signals_names) != m:
        raise ValueError("'signals' and 'signals_name' must have the same size")

    # Plot and errors
    for i in range(m):
        if len(signals[i]) != n:
            msg = "WARNING : All signal of 'signals' must by have a length equals to {} (length of x vector). Error " \
                  "occurred for signal {}".format(n, i)
            print(warningText(msg))
            continue
        plt.plot(x, signals[i], label=signals_names[i])

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

    if title is not False:
        plt.title(title)

    # fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    if saving:
        frame = str(input('Frame : '))
        trans = bool(input('Transparent image ? (bool) : '))
        datas = str(input('Data\'s ? (False or str) : '))
        plt.savefig(frame, transparent=trans, metadata={'Description': datas})


if __name__ == '__main__':
    pass
