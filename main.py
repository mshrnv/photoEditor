import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from photoeditor import PhotoEditorGUI

if __name__ == "__main__":

    # Создание приложения QT
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    # Инициализация окна фоторедактора и его отображение
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
