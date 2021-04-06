# ============================================== #
# Main program file                              #
# Author : Quentin Prieels                       #
# Date : April 2021                              #
# Version 1.0                                    #
# ============================================== #

def warningText(text):
    """
    Create a warning text.
    :param text: Message of error
    :return: Text in red color in format Warning : <text>
    :rtype: str
    """
    return '\033[91m' + "WARNING : {}".format(str(text)) + '\033[0m'


if __name__ == '__main__':
    pass
