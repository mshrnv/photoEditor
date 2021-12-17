
from PyQt5 import QtCore, QtGui, QtWidgets


class AuthGui(object):
    """Класс используется для работы с окном авторизации пользователей"""

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(500, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setGeometry(QtCore.QRect(190, 210, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.auth_button.setFont(font)
        self.auth_button.setAutoFillBackground(False)
        self.auth_button.setCheckable(False)
        self.auth_button.setObjectName("auth_button")

        self.login_input = QtWidgets.QLineEdit(self.centralwidget)
        self.login_input.setGeometry(QtCore.QRect(140, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_input.setFont(font)
        self.login_input.setText("")
        self.login_input.setAlignment(QtCore.Qt.AlignCenter)
        self.login_input.setObjectName("login_input")

        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(140, 150, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_input.setFont(font)
        self.password_input.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.password_input.setText("")
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setObjectName("password_input")

        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(200, 110, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")

        self.login_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.login_label.setFont(font)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setObjectName("login_label")
        self.login_label.setGeometry(QtCore.QRect(210, 40, 81, 21))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 513, 21))
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход в приложение"))
        self.auth_button.setText(_translate("MainWindow", "Войти"))
        self.password_label.setText(_translate("MainWindow", "Пароль"))
        self.login_label.setText(_translate("MainWindow", "Логин"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AuthGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
