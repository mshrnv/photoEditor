import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QSizePolicy, QScrollArea
from PyQt5.QtGui import QPixmap, QImage, QPalette
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
        # Choosing the file
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
            # User pressed 'cancel'
            pass
        else:
            # Some errors
            QMessageBox.information(self, "Error", 
                "Cannot to open the file.", QMessageBox.Ok)

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
        self.image_label = imageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        #self.scroll_area.setWidgetResizable(False)
        #scroll_area.setMinimumSize(800, 800)
        
        self.scroll_area.setWidget(self.image_label)
        #self.scroll_area.setVisible(False)

        self.setCentralWidget(self.scroll_area)

        #self.resize(QApplication.primaryScreen().availableSize() * 3 / 5)

    def createEditingBar(self):
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

        # Create editing tool buttons
        filters_label = QLabel("Filters")

        convert_to_grayscale = QToolButton()
        #convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        #convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        convert_to_RGB = QToolButton()
        #convert_to_RGB.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        #convert_to_RGB.clicked.connect(self.image_label.convertToRGB)

        convert_to_sepia = QToolButton()
        #convert_to_sepia.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        #convert_to_sepia.clicked.connect(self.image_label.convertToSepia)

        change_hue = QToolButton()
        change_hue.setIcon(QIcon(os.path.join(icon_path, "")))
        #change_hue.clicked.connect(self.image_label.changeHue)

        brightness_label = QLabel("Brightness")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-255, 255)
        self.brightness_slider.setTickInterval(35)
        self.brightness_slider.setTickPosition(QSlider.TicksAbove)
        #self.brightness_slider.valueChanged.connect(self.image_label.changeBrighteness)

        contrast_label = QLabel("Contrast")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-255, 255)
        self.contrast_slider.setTickInterval(35)
        self.contrast_slider.setTickPosition(QSlider.TicksAbove)
        #self.contrast_slider.valueChanged.connect(self.image_label.changeContrast)

        # Set layout for dock widget
        editing_grid = QGridLayout()
        #editing_grid.addWidget(filters_label, 0, 0, 0, 2, Qt.AlignTop)
        editing_grid.addWidget(convert_to_grayscale, 1, 0)
        editing_grid.addWidget(convert_to_RGB, 1, 1)
        editing_grid.addWidget(convert_to_sepia, 2, 0)
        editing_grid.addWidget(change_hue, 2, 1)
        editing_grid.addWidget(brightness_label, 3, 0)
        editing_grid.addWidget(self.brightness_slider, 4, 0, 1, 0)
        editing_grid.addWidget(contrast_label, 5, 0)
        editing_grid.addWidget(self.contrast_slider, 6, 0, 1, 0)
        editing_grid.setRowStretch(7, 10)

        container = QWidget()
        container.setLayout(editing_grid)

        self.editing_bar.setWidget(container)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.editing_bar)

        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def createMenu(self):
        pass

    def createToolBar(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    #app.setStyleSheet(style_sheet)
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
