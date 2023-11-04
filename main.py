import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("UI_test/main_window.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.open)

    #initial testing
    def open(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        f = open(path,"r")
        st = ""
        for line in f.readlines():
            st = st + line
            st = st + "\n"

        self.textBrowser.setText(st)
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()
    #lol
    #la


if __name__ == '__main__':
    main()

#
