"""
    Импорт необходимых библиотек для запуска приложения
"""
import sys
import PyQt5
from gui import AuthGui

if __name__ == "__main__":

    # Создание приложения QT
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    app.setAttribute(PyQt5.QtCore.Qt.AA_DontShowIconsInMenus, True)

    # Инициализация окна авторизации и его отображение
    window = AuthGui()
    window.show()
    sys.exit(app.exec_())
    