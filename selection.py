import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

ICON_PATH = 'icons'

class SelectionGui(QMainWindow):

    def __init__(self, images = list()):
        """Констрктор класса SelectionGui"""

        self.images = images
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Главный метод, создающий окно и рисующий все компоненты"""

        self.setFixedSize(540, 360)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.createCentralWidget()

        # Показ окна
        self.show()

    def createCentralWidget(self):

        # font = QtGui.QFont()
        # font.setFamily("Calibri")
        # font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)
        # MainWindow.setFont(font)

        # Центральный (главный) виджет окна
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # Сетка с компонентами окна
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
        self.load_button.setText("Загрузить")
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
        self.edit_button.setText("Редактировать")
        self.gridLayout.addWidget(self.edit_button, 1, 0, 1, 1)

        self.exit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Выйти")
        self.gridLayout.addWidget(self.exit_button, 4, 0, 1, 1)

        self.list = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.list.setObjectName("list")
        
        for image in self.images:
            item = QtWidgets.QListWidgetItem()
            item.setText(image)
            self.list.addItem(item)

        self.gridLayout.addWidget(self.list, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    # Создание приложения QT
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    # Инициализация окна фоторедактора и его отображение
    window = SelectionGui(['1.jpg', '2.png'])
    sys.exit(app.exec_())
