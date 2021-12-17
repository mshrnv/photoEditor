import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

ICON_PATH = 'icons'

class AuthGui(QMainWindow):
    """Класс используется для работы с окном авторизации пользователей"""

    def __init__(self):
        """Констрктор класса AuthGui"""

        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Главный метод, создающий окно и рисующий все компоненты"""

        self.setFixedSize(500, 300)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.createCentralWidget()

        # Показ окна
        self.show()

    def createCentralWidget(self):
        """Метод, инициализирующий все компоненты окна"""
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Войти"
        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setText('Войти')
        self.auth_button.setGeometry(QtCore.QRect(190, 210, 131, 51))
        self.auth_button.clicked.connect(self.auth)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.auth_button.setFont(font)
        self.auth_button.setAutoFillBackground(False)
        self.auth_button.setCheckable(False)
        self.auth_button.setObjectName("auth_button")

        # Поле ввода логина
        self.login_input = QtWidgets.QLineEdit(self.centralwidget)
        self.login_input.setGeometry(QtCore.QRect(140, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_input.setFont(font)
        self.login_input.setText("")
        self.login_input.setAlignment(QtCore.Qt.AlignCenter)
        self.login_input.setObjectName("login_input")

        # Поле ввода пароля
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(140, 150, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_input.setFont(font)
        self.password_input.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.password_input.setText("")
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setObjectName("password_input")

        # Надпись "Пароль"
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setText('Пароль')
        self.password_label.setGeometry(QtCore.QRect(200, 110, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")

        # Надпись "Логин"
        self.login_label = QtWidgets.QLabel()
        self.login_label.setText('Логин')
        self.login_label.setGeometry(QtCore.QRect(210, 40, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.login_label.setFont(font)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setObjectName("login_label")
        
        # Grid widget (сетка)
        editing_grid = QGridLayout()
        editing_grid.addWidget(self.login_label, 1, 0, 1, 0)
        editing_grid.addWidget(self.login_input, 2, 0, 1, 0)
        editing_grid.addWidget(self.password_label, 3, 0, 1, 0)
        editing_grid.addWidget(self.password_input, 4, 0, 1, 0)
        editing_grid.addWidget(self.auth_button, 5, 0, 1, 0)

        editing_grid.setRowStretch(6, 7)

        # Инициализация виджета, используя сетку
        container = QWidget()
        container.setLayout(editing_grid)

        self.setCentralWidget(container)

    def auth(self):
        """Функция проверяет введенные данные и определяет дальнейшее действие"""
        
        username = self.login_input.text()
        password = self.password_input.text()
        print(username, password, sep=" ")
        self.close()

# if __name__ == "__main__":

#     # Создание приложения QT
#     app = QApplication(sys.argv)
#     app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

#     # Инициализация окна авторизации и его отображение
#     window = AuthGui()
#     sys.exit(app.exec_())
