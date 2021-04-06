# ================================= #
# ReaderCSV Class only              #
# Author : Quentin Prieels          #
# Date : April 2021                 #
# Version 1.3                       #
# ================================= #

# Packages
import numpy as np

# From project files
from main.plots import plotSignals
from main.main import warningText


class ReaderCSV:
    """
    This class allows to read CSV files and to use them to make graphs. Each object must be a CSV file with the
    following structure:

        <name x axis>;<name signal 1>;<name signal 2>;...;<name signal m>
        <unit x axis>;<unit signal 1>;<unit signal 2>;...;<unit signal m>
        # Blank line
        <x1 value>;<y1 value signal 1>;<y1 value signal 2>;... ;<y1 value signal m>
        <x2 value>;<y2 value signal 1>;<y2 value signal 2>;... ;<y2 value signal m>
        ...
        <xm value>;<ym value signal 1>;<ym value signal 2>;... ;<ym value signal m>

    So there are m different signals ALL WITH THE SAME UNIT (except the x-axis) but in orders of magnitude that can be
    different. The units and their orders of magnitude accepted are:

        ===================================================
        == Name     : Symbols used (do not use the name) ==
        == Volt     : kV, V, mV, iV, nV, pV              ==
        == Ampere   : kA, A, mA, iA, nA, pA              ==
        == Ohms     : kO, O, mO, iA, nO, pO              ==
        == Hertz    : kH, H, mH, iH, nH, pH              ==
        ===================================================

    These units are only valid for the different signals (y-axis).
    """

    # Class Variables
    __units = {'V': 'Tension',
               'A': 'Ampère',
               'O': 'Ohms',
               'H': 'Hertz'}
    __orders = {'k': 1000,
                '': 1,
                'm': 0.001,
                'i': 0.000001,
                'n': 0.000000001,
                'p': 0.0000000000001}

    # Constructor
    def __init__(self, filepath, filename, signals_names, preferred_unit='V'):
        """
        :param filepath: Location of the CSV file
        :param filename: Name of the file
        :param signals_names: Names of the signals
        :param preferred_unit: Unit to be use for the y-axis.
        """
        # File infos
        self.__path = filepath
        self.__name = filename

        # Signals infos
        self.__signalsNames = signals_names
        self.__numberSignals = self.findSignalsNumbers()
        self.__signalsUnits = self.findUnits()[0]

        # Units infos
        self.__preferredUnit = preferred_unit
        self.__axisUnits = self.findAxisUnits()

        # Axis info
        self.__axisNames = self.findAxisNames()

    # Accessor methods
    def getPath(self):
        """
        :return: Path of CSV file
        :rtype: str
        """
        return self.__path

    def getName(self):
        """
        :return: Name of file
        :rtype: str
        """
        return self.__name

    def getNumberSignals(self):
        """
        :return: Number of signals (curve that will be draw)
        :rtype: int
        """
        return self.__numberSignals

    def getSignalsNames(self):
        """
        :return: Name(s) of the signals
        :rtype: list
        """
        return self.__signalsNames

    def getSignalsUnits(self):
        """
        :return: Units in which the signals are expressed
        :rtype: list
        """
        return self.__signalsUnits

    def getPreferredUnit(self):
        """
        :return: The unit that will be use for all signals when there are plot (also onto y-axis name)
        :rtype: str
        """
        return self.__preferredUnit

    def getAxisUnits(self):
        """
        :return: The units of the x and y axis
        :rtype: list
        """
        return self.__axisUnits

    def getAxisNames(self):
        """
        :return: The names of the x and y axis
        :rtype: list
        """
        return self.__axisNames

    # Mutator methods
    def setName(self, new_name):
        """
        Change the name of the object and check that the length of the new name is behind 144 charters.
        :param new_name: New name for the title of the plot
        :type new_name: str
        :return: Nothing, it just change the instance variable __name
        """
        if len(new_name) <= 144:
            old_name = self.getName()
            self.__name = str(new_name)
            print('Name {} is change by {}.'.format(old_name, self.getName()))
        else:
            msg = "The requested name has a length of more than 144 characters, please change the name."
            print(warningText(msg))

    def setPreferredUnit(self, unit):
        """
        Changes the unit used to represent the graphs. What is most important is the prefix and therefore the order of
        magnitude. Be careful not to change the unit itself, otherwise the names of the axes will also be changed. It
        also check that the unit is correct and usable (see the definition of the class).
        :param unit: New unit to use
        :type unit: str
        """
        if self.checkUnit(unit):
            old_unit = self.getPreferredUnit()
            self.__preferredUnit = unit
            self.__axisUnits = self.findAxisUnits()
            print('Preferred unit {} is change by {}.'.format(old_unit, self.getPreferredUnit()))
        else:
            msg = "This unit is not usable. Please change the unit. Current unit: {}".format(self.getPreferredUnit())
            print(warningText(msg))

    def setAxisNames(self, x_axis, y_axis):
        """
        Change the name of the x and y axis.
        :param x_axis: New name for x axis
        :param y_axis: New name for y axis
        """
        old_names = self.getAxisNames()
        self.__axisNames = [x_axis, y_axis]
        print('Axis names {} is change by {}.'.format(old_names, self.getAxisNames()))

    # Knowledge methods
    def findSignalsNumbers(self):
        """
        Find the number of signals that are in the CSV file. The function does not count the x axis as a signal. A CSV
        file with 3 numbers
            (x; signal 1; signal 2)
        will have 2 signals.
        :return: The number of signals
        :rtype: int
        """
        with open(self.getPath(), 'r') as file:
            first_line = file.readline().strip().split(';')
        return len(first_line) - 1

    def findUnits(self):
        """
        Find the units needed to run the program. We find the units of the x-axis and the unit in which each signal is
        expressed.
        :return: The different units in the form [[signal unit], x-axis unit]
        :rtype: list
        """
        with open(self.getPath(), 'r') as file:
            # Get units
            second_line = file.readlines()[1]
            units = second_line.strip().replace('(', '').replace(')', '').split(';')

            # Check units
            for unit in units[1:]:
                if not self.checkUnit(unit):
                    raise ValueError('This unit ({})can not be use'.format(unit))

        return units[1:], units[0]

    def findAxisUnits(self):
        """
        Find the unit of each axis
        :return: The unit of x and y axis [x axis, y axis]
        :rtype: list
        """
        return [self.findUnits()[1], self.getPreferredUnit()]

    def findAxisNames(self):
        """
        Find the name of each axis. The name of x axis is the name that is given bt the CSV file (first word at first
        line => see CSV structure that is use in the class description). The name of y axis is deduced from the unit of
        signals.
        :return: The name of x and y axis
        :rtype: list
        """
        # x-axis
        with open(self.getPath(), 'r') as file:
            x_axis_name = file.readline().strip().split(';')[0]

        # y-axis
        try:
            y_axis_name = self.__units[self.getPreferredUnit()[-1]]
        except:
            y_axis_name = 'Error !'
            msg = "y-axis name can not be define, please define them manually."
            print(warningText(msg))

        return [x_axis_name, y_axis_name]

    def unitsChange(self, number, old_unit, new_unit):
        """
        Gives the value of a number in a desired unit from another unit
        :param number: Number to use
        :type number: float
        :param old_unit: Actual unit of this number
        :type old_unit: str
        :param new_unit: Unit of the new number
        :type new_unit: str
        :return: The value of the number into the new unit
        :rtype float
        """
        try:
            # Old unit into standard unit
            if old_unit in self.__units:
                standard_unit = number
            else:
                standard_unit = number * self.__orders[old_unit[0]]

            # Standard unit into new unit
            if new_unit in self.__units:
                return standard_unit
            else:
                return standard_unit / self.__orders[new_unit[0]]

        except:
            ValueError('An error occurred during the transformation of units')

    # Plot methods
    def makeSignals(self, precision=1):
        """
        Create numpy array with the different signals that can be
        :param precision: Allows to take only a part of the data in the file. This value MUST BE positive
        :type precision: int
        :return: Return the x list (list of all x-axis points) of size n and a numpy matrix of m signals and length n
        :rtype: tuple
        """
        # Create the arguments of plotSignals function (see plotsTest.py > plotSignal)
        with open(self.getPath(), 'r') as file:
            lines = file.readlines()[3:]
            n = len(lines)
            m = self.getNumberSignals()
            x = np.zeros(n)
            signals = np.zeros((m, n))
            for i in range(0, n, precision):
                for j in range(m + 1):
                    line = lines[i].strip().split(";")
                    if j == 0:
                        x[i] = float(line[j].replace(',', '.'))
                    else:
                        number = float(line[j].replace(',', '.'))
                        signal_value = self.unitsChange(number, self.getSignalsUnits()[j - 1],
                                                        self.getPreferredUnit())
                        signals[j - 1][i] = signal_value

        return x, signals

    def plot(self, precision=1, title=False):
        """
        Displays the data from the CSV file as a graph.
        :param precision: Allows to take only a part of the data in the file. This value MUST BE positive
        :type precision: int
        :param title: Know of the plot must have a title or not
        :type title: bool
        :return: Create a plot
        """
        # Create the arguments of plotSignals function (see plotsTest.py > plotSignal)
        x, signals = self.makeSignals(precision)

        x_axis_name = self.getAxisNames()[0] + " [" + self.getAxisUnits()[0] + "]"
        y_axis_name = self.getAxisNames()[1] + " [" + self.getAxisUnits()[1] + "]"

        # Use of plot function
        if title:
            plotSignals(x, signals, self.getSignalsNames(), x_label=x_axis_name, y_label=y_axis_name,
                        title=self.getName())
        else:
            plotSignals(x, signals, self.getSignalsNames(), x_label=x_axis_name, y_label=y_axis_name)

    # Magic Methods
    def __str__(self):
        """
        :return: A string representation of the most useful data of the CSV file
        :rtype: str
        """
        n = self.getNumberSignals()
        text = '\n=====================================================================\n'
        text += 'This are informations about \33[94m{}\033[0m file, locate at \33[94m{}\033[0m. \n'\
            .format(self.getName(), self.getPath())
        text += 'Number of Signals : {} \n'.format(n)
        for i in range(0, n):
            text += '\t - {} ({}) \n'.format(self.getSignalsNames()[i], self.getSignalsUnits()[i])
        text += 'Preferred unit is  {}.\n'.format(self.getPreferredUnit())
        text += 'Axis are : {} ({}) (x-axis) and {} ({}) (y-axis)\n'.format(self.getAxisNames()[0],
                                                                            self.getAxisUnits()[0],
                                                                            self.getAxisNames()[1],
                                                                            self.getAxisUnits()[1])
        text += '=====================================================================\n'
        return text

    # Check method
    def checkUnit(self, unit):
        """
        Verifies that the unit is consistent with the unit the class is considering
        :param unit: Unit to check
        :return: True or False, it depend of the unit is correct or not
        :rtype: bool
        """
        if unit[-1] in self.__units:
            if len(unit) == 2 and unit[0] in self.__orders:
                return True
            elif len(unit) == 1:
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    test = ReaderCSV('../../data/exemple.csv', 'test', ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4'])
    test.plot()
