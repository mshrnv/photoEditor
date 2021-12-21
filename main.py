import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui import AuthGui

if __name__ == "__main__":

    # Создание приложения QT
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    # Инициализация окна авторизации и его отображение
    window = AuthGui()
    window.show()
    sys.exit(app.exec_())
