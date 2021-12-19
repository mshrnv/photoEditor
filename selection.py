import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

ICON_PATH = 'icons'


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 358)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 471, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.load_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.load_button.setFont(font)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 3, 0, 1, 1)
        self.edit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.edit_button.setFont(font)
        self.edit_button.setStyleSheet("")
        self.edit_button.setObjectName("edit_button")
        self.gridLayout.addWidget(self.edit_button, 1, 0, 1, 1)
        self.exit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.gridLayout.addWidget(self.exit_button, 4, 0, 1, 1)
        self.list = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.list.setObjectName("list")
        item = QtWidgets.QListWidgetItem()
        self.list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list.addItem(item)
        self.gridLayout.addWidget(self.list, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_button.setText(_translate("MainWindow", "Загрузить"))
        self.edit_button.setText(_translate("MainWindow", "Редактировать"))
        self.exit_button.setText(_translate("MainWindow", "Выйти"))
        __sortingEnabled = self.list.isSortingEnabled()
        self.list.setSortingEnabled(False)
        item = self.list.item(0)
        item.setText(_translate("MainWindow", "1.jpeg"))
        item = self.list.item(1)
        item.setText(_translate("MainWindow", "2.jpeg"))
        item = self.list.item(2)
        item.setText(_translate("MainWindow", "3.png"))
        self.list.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
