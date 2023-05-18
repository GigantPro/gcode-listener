import sys

from PyQt5 import QtWidgets

from .controller import Controller


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    app.exec_()


if __name__ == '__main__':
    main()
