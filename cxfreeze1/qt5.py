import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication


def main():
    app = QtWidgets.QApplication(sys.argv)  # type: QApplication
    widget = QtWidgets.QWidget()
    widget.show()
    app.exec()


if __name__ == '__main__':
    main()