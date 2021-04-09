# ============================================== #
# Plots functions                                #
# Author : Quentin Prieels                       #
# Date : April 2021                              #
# Version 1.0                                    #
# ============================================== #

# Package
import matplotlib.pyplot as plt

# From project files
from main.main import warningText


def plotSignals(x, signals, signals_names, x_label="", y_label="", title="", saving=False):
    """
    Plot the different signals of the signals list as function of x
    :param x: List of dimension n containing the abscissas at which the signals are evaluated
    :param signals: List m by n of m signals evaluate in n points (the points of x list)
    :param signals_names: List of dimension m containing all the names of the signals
    :param x_label: Name of horizontal axis
    :param y_label: Name of the vertical axis
    :param title: Title of the plot figure
    :param saving: To know of the plot will be save or not
    :return: Show a plot of all the signals into a unique graph
    """
    # Size of parameters
    n = len(x)
    m = len(signals)

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
    if title is not False:
        plt.title(title)
    plt.show()
    if saving:
        frame = str(input('Frame : '))
        trans = bool(input('Transparent image ? (bool) : '))
        datas = str(input('Data\'s ? (False or str) : '))
        plt.savefig(frame, transparent=trans, metadata={'Description': datas})


if __name__ == '__main__':
    pass
