import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class imageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent 
        self.image = QImage()
        #self.image = "images/parrot.png"

        #self.original_image = self.image.copy
        self.original_image = self.image

        #self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        # setBackgroundRole() will create a bg for the image
        #self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(True)

        # Load image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

    def openImage(self):
        # Окно выбора файла
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg )")

        if image_file:
            self.parent.zoom_factor = 1
            #self.parent.scroll_area.setVisible(True)
            #self.parent.print_act.setEnabled(True)
            #self.parent.updateActions()

            # Reset all sliders
            self.parent.brightness_slider.setValue(0)

            # Get image format
            image_format = self.image.format()
            self.image = QImage(image_file)
            self.original_image = self.image.copy()

            #pixmap = QPixmap(image_file)
            self.setPixmap(QPixmap().fromImage(self.image))
            #image_size = self.image_label.sizeHint()
            self.resize(self.pixmap().size())
        elif image_file == "":
            # Пользователь выбрал 'Назад'
            pass
        else:
            # Не получилось открыть файл
            QMessageBox.information(self, "Ошибка", 
                "Невозможно открыть файл.", QMessageBox.Ok)

class PhotoEditorGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initializeUI()

        self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Photo Editor")
        self.showMaximized()

        self.zoom_factor = 1

        self.createMainLabel()
        self.createEditingBar()
        self.createMenu()
        self.createToolBar()

        self.show()

    def createMainLabel(self):
        pass

    def createEditingBar(self):
        pass

    def createMenu(self):
        pass

    def createToolBar(self):
        pass
