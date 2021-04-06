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


class Signal:

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

        # y axis and relation
        if f is not None and y is None:
            self.__f = f
            self.__y = f(x)
            pass

        # Equation and y : compare and ask witch are the good
        elif f is not None and y is not None:
            self.__f = f
            self.__y = y
            # todo: Compare signals

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

        # Axis Names
        self.__axisNames = self.findAxisNames()

    # Accessors methods
    def getName(self):
        return self.__name

    def getUnits(self):
        return self.__units

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getF(self):
        return self.__f

    # Mutator methods
    def setName(self, name):
        old_name = self.getName()
        self.__name = name
        print("Name {} successfully change by {}.".format(old_name, self.getName()))

    def setUnits(self, new_x_unit, new_y_unit):
        pass

    # Knowledge methods
    def plot(self, precision=1):
        pass

    def findAxisNames(self):
        pass

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

    # Check methods
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

    def compareSignal(self):
        pass


class Block:

    def __init__(self, name, in_signals, out_signal, f):
        pass


if __name__ == '__main__':
    pass
