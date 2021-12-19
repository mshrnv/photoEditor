import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
#from photoeditor import PhotoEditorGUI

ICON_PATH = 'icons' # Путь к иконкам приложения

class SelectionGui(QMainWindow):
    """Класс используется для работы с окном выбора изображения"""

    def __init__(self, username, images = list()):
        """Констрктор класса SelectionGui"""

        self.images   = images
        self.username = username
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
        # self.show()

    def createCentralWidget(self):
        """Функция, создающая все компоненты окна"""

        # Центральный (главный) виджет окна
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)

        # Сетка с компонентами окна
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 471, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Кнопка "Загрузить"
        self.load_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.load_button.setObjectName("load_button")
        self.load_button.setText("Загрузить")
        self.load_button.clicked.connect(self.loadImage)
        self.gridLayout.addWidget(self.load_button, 3, 0, 1, 1)

        # Кнопка "Редактировать"
        self.edit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setText("Редактировать")
        self.edit_button.clicked.connect(self.editImage)
        self.gridLayout.addWidget(self.edit_button, 1, 0, 1, 1)

        # Кнопка "Выйти"
        self.exit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Выйти")
        self.exit_button.clicked.connect(self.exit)
        self.gridLayout.addWidget(self.exit_button, 4, 0, 1, 1)

        # Элемент - список изображений
        self.list = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.list.setObjectName("list")
        
        # Добавление фотографий в список для отображения на экране
        for image in self.images:
            item = QtWidgets.QListWidgetItem()
            item.setText(image)
            self.list.addItem(item)

        self.gridLayout.addWidget(self.list, 0, 0, 1, 1)

        # Установка главного виджета
        self.setCentralWidget(self.centralwidget)

    def editImage(self):
        """Функция предназначена для открытия окна фоторедактора"""
        # Здеь будет открываться окно редактирования
        print('Редактирование')
        pass

    def loadImage(self):
        """Функция предназначена для загрузки изображения в базу"""
        # Диалоговое окно выбора изображения
        # Запись в БД
        print('Загрузка')
        pass

    def exit(self):
        """Функция предназначена для выхода из сессии пользователя"""
        # Закрытие окна, открытие другого
        print('Выход')
        pass

# if __name__ == "__main__":
#     # Создание приложения QT
#     app = QApplication(sys.argv)
#     app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

#     # Инициализация окна фоторедактора и его отображение
#     window = SelectionGui(['1.jpg', '2.png'])
#     sys.exit(app.exec_())