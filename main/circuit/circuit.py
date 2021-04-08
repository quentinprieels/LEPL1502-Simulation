# ======================================== #
# Classes needed to represent a circuit    #
# Author : Quentin Prieels                 #
# Date : April 2021                        #
# Version 1.4                              #
# ======================================== #
# Packages
import numpy as np

# From project files
from main.main import warningText
from main.plots import plotSignals


class Signal:
    # Class Variables
    __units_d = {'V': 'Tension',
                 'A': 'Ampère',
                 'O': 'Ohms',
                 'H': 'Hertz'}
    __orders = {'k': 1000,
                '': 1,
                'm': 0.001,
                'i': 0.000001,
                'n': 0.000000001,
                'p': 0.0000000000001,
                'V': 1,
                'A': 1,
                'H': 1,
                'O': 1}

    def __init__(self, name, units, x, y=None, f=None):
        # Name
        self.__name = str(name)

        # Units
        if len(units) == 2:
            self.__units = units
        else:
            msg = "Units must be a list of size 2 (for x and y axis). Please define units !"
            print(warningText(msg))
            self.__units = None

        # x-axis
        self.__x = np.array(x)

        # Axis Names
        self.__axisNames = self.findAxisNames()

        # y axis and relation
        if f is not None and y is None:
            self.__f = f
            self.__y = f(x)
            pass

        # Equation and y : compare and ask witch are the good
        elif f is not None and y is not None:
            self.__f = f
            self.__y = y
            self.autoCompareSignal()

        # Not equation and y : create y
        elif f is None and y is not None:
            self.__y = y
            self.__f = None
            msg = "No function has been defined."
            print(warningText(msg))

        # Not equation and not y : say and None
        else:
            msg = "No possibility to interpret the signal. Neither the ordinates nor a function has been defined. " \
                  "Please define at least one of the two parameters"
            print(warningText(msg))
            self.__y = None
            self.__f = None

    # Accessors methods
    def getName(self):
        return self.__name

    def getUnits(self):
        return self.__units

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getF(self, x):
        return self.__f(x)

    def getAxisNames(self):
        return self.__axisNames

    def getAxisLabels(self):
        x_axis_name = self.getAxisNames()[0] + " [" + self.getUnits()[0] + "]"
        y_axis_name = self.getAxisNames()[1] + " [" + self.getUnits()[1] + "]"
        return x_axis_name, y_axis_name

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

    def setUnit(self, new_y_unit):
        if self.checkUnit(new_y_unit):
            old_unit = self.getUnits()[1]
            self.__units[1] = new_y_unit
            coeff = self.findCoeff('V', new_y_unit)
            self.__y = self.getF(coeff * self.getX())
            print("Unit of signal changed form {} to {}. Y-axis value are now {} time bigger that the original signal "
                  "(unit with coeff 1).".format(old_unit, new_y_unit, coeff))
            msg = "We use the function, not the y value to change the curve !"
            print(warningText(msg))

        else:
            msg = "Incorrect unit value, unit of y-axis is currently {}.".format(self.getUnits()[1])
            print(warningText(msg))

    def setAxisNames(self, x_axis, y_axis):
        old_names = self.getAxisNames()
        self.__axisNames = [str(x_axis), str(y_axis)]
        print('Name of axis {} where changed by {}'.format(old_names, self.getAxisNames()))

    # Knowledge methods
    def plot(self, title=False, saving=False):
        plotSignals(self.getX(), [self.getY()], [self.getName()], x_label=self.getAxisLabels()[0],
                    y_label=self.getAxisLabels()[1], title=title, saving=saving)

    def findAxisNames(self):
        axis_names = ['Unknown', 'Unknown']
        if 's' in self.getUnits()[0]:
            axis_names[0] = 'Temps'

        try:
            axis_names[1] = self.__units_d[self.getUnits()[1][-1]]
        except KeyError:
            msg = "y-axis name can not be define, please define them manually."
            print(warningText(msg))

        return axis_names

    def findCoeff(self, old_unit, new_unit):
        """
        Gives the value of a number in a desired unit from another unit
        :param old_unit: Actual unit of this number
        :type old_unit: str
        :param new_unit: Unit of the new number
        :type new_unit: str
        :return: The value of the number into the new unit
        :rtype float
        """
        try:
            coeff = self.__orders[old_unit[0]] / self.__orders[new_unit[0]]

            return coeff

        except:
            ValueError('An error occurred during the transformation of units, impossible to find the correct '
                       'coefficient')

    # Check methods
    def checkUnit(self, unit):
        """
        Verifies that the unit is consistent with the unit the class is considering
        :param unit: Unit to check
        :return: True or False, it depend of the unit is correct or not
        :rtype: bool
        """
        if unit[-1] in self.__units_d:
            if len(unit) == 2 and unit[0] in self.__orders:
                return True
            elif len(unit) == 1:
                return True
            else:
                return False
        else:
            return False

    def autoCompareSignal(self):
        msg = "An equation and a value of y have been given. Here is the comparison of the 2."

        plotSignals(self.getX(), [self.getY(), self.getF(self.getX())], ['Y list', 'Function'],
                    x_label=self.getAxisLabels()[0], y_label=self.getAxisLabels()[1])
        print(warningText(msg))

    def compareSignals(self, *args, title=False, saving=False):
        """
        :param args:
        :type args: Signal
        :return:
        """
        signals_names = [self.getName()]
        signals = [self.getY()]
        for arg in args:
            if len(arg.getY()) == len(self.getX()):
                signals_names.append(arg.getName())
                signals.append(arg.getY())
            else:
                msg = "Signal {} have not a length of {}, comparaison can not be done. This signal is ignored". \
                    format(arg.getName(), len(self.getX()))
                print(warningText(msg))
                continue
        plotSignals(self.getX(), signals, signals_names, x_label=self.getAxisLabels()[0],
                    y_label=self.getAxisLabels()[1], title=title, saving=saving)


"""
class Block:

    def __init__(self, name, in_signals, out_signal=None, f=None):
        """
"""
        :param name:
        :param in_signals:
        :type in_signals: list of Signal
        :param out_signal:
        :type out_signal: Signal
        """
"""
        self.__name = str(name)
        self.__inSignals = in_signals
        self.__outSignal = out_signal
        self.__f = f

    # Accessor methods
    def getName(self):
        return self.__name

    def getInSignals(self):
        return self.__inSignals

    def getOutSignals(self):
        return self.__outSignal

    def getF(self):
        return self.__f

    # Mutator methods
    def setName(self, new_name):
        """
"""
        Change the name of the object and check that the length of the new name is behind 144 charters.
        :param new_name: New name for the title of the plot
        :type new_name: str
        :return: Nothing, it just change the instance variable __name
        """
"""
        if len(new_name) <= 144:
            old_name = self.getName()
            self.__name = str(new_name)
            print('Name {} is change by {}.'.format(old_name, self.getName()))
        else:
            msg = "The requested name has a length of more than 144 characters, please change the name."
            print(warningText(msg))

    # Make method
    def makeOutSignal(self):
        return Signal(self.getName() + " - Out Signal", self.getInSignals()[0].getUnits(),
                      self.getInSignals()[0].getX(), self.getF())

    @staticmethod
    def checkSignal(signal):
        return isinstance(signal, Signal)
"""

if __name__ == '__main__':
    pass
