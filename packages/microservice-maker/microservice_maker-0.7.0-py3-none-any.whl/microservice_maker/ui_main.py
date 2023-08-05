import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from microservice_maker.ui_django import UiMainUi


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainUi()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
