import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Scanner import Scanner


class MyGUI(QMainWindow):


    def __init__(self):
        self.filePath = " "
        super(MyGUI, self).__init__()
        uic.loadUi("UI_test/main_window.ui", self)
        self.show()
        self.pushButton.clicked.connect(self.choose)
        self.pushButton_2.clicked.connect(self.scan)
    # initial testing


    def choose(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.filePath = path
        f = open(path, "r",encoding='utf-8').read()
        self.textBrowser.setText(f)


    def scan(self):
        obj = Scanner()
        obj.tokenize(self.filePath)
        obj.export()
        f = open("output.txt", "r",encoding='utf-8').read()

        self.textBrowser_2.setText(f)

def main():
    app = QApplication([])
    window = MyGUI()
    window.setWindowTitle("Scanner")
    app.exec_()


if __name__ == '__main__':
    main()
