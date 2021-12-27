from PyQt5.QtWidgets import QMessageBox, QMainWindow

class Error(QMainWindow):
    
    def __init__(self, parent, error_message):
        QMessageBox.warning(parent, "Ошибка", error_message)