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
        about_act = QAction('About', self)
        #about_act.triggered.connect(self.aboutDialog)

        #self.exit_act = QAction(QIcon(os.path.join(icon_path, "exit.png")), 'Quit Photo Editor', self)
        self.exit_act.setShortcut('Ctrl+Q')
        #self.exit_act.triggered.connect(self.close)

        #---------------------

        #self.new_act = QAction(QIcon(os.path.join(icon_path, "new.png")), 'New...')

        #self.open_act = QAction(QIcon(os.path.join(icon_path, "open.png")),'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        #self.open_act.triggered.connect(self.image_label.openImage)

        #self.save_act = QAction(QIcon(os.path.join(icon_path, "save.png")), "Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        #self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        #---------------------------

        #self.revert_act = QAction("Revert to Original", self)
        #self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        #--------------------------

        #self.crop_act = QAction(QIcon(os.path.join(icon_path, "crop.png")), "Crop", self)
        self.crop_act.setShortcut('Shift+X')
        #self.crop_act.triggered.connect(self.image_label.cropImage)

        #self.resize_act = QAction(QIcon(os.path.join(icon_path, "resize.png")), "Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        #self.resize_act.triggered.connect(self.image_label.resizeImage)

        #self.rotate90_cw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_cw.png")),'Rotate 90º CW', self)
        #self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))

        #self.rotate90_ccw_act = QAction(QIcon(os.path.join(icon_path, "rotate90_ccw.png")),'Rotate 90º CCW', self)
        #self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))

        #self.flip_horizontal = QAction(QIcon(os.path.join(icon_path, "flip_horizontal.png")), 'Flip Horizontal', self)
        #self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))

        #self.flip_vertical = QAction(QIcon(os.path.join(icon_path, "flip_vertical.png")), 'Flip Vertical', self)
        #self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        
        #self.zoom_in_act = QAction(QIcon(os.path.join(icon_path, "zoom_in.png")), 'Zoom In', self)
        self.zoom_in_act.setShortcut('Ctrl++')
        #self.zoom_in_act.triggered.connect(lambda: self.zoomOnImage(1.25))
        self.zoom_in_act.setEnabled(False)

        #self.zoom_out_act = QAction(QIcon(os.path.join(icon_path, "zoom_out.png")), 'Zoom Out', self)
        self.zoom_out_act.setShortcut('Ctrl+-')
        #self.zoom_out_act.triggered.connect(lambda: self.zoomOnImage(0.8))
        self.zoom_out_act.setEnabled(False)

        #self.normal_size_Act = QAction("Normal Size", self)
        self.normal_size_Act.setShortcut('Ctrl+=')
        #self.normal_size_Act.triggered.connect(self.normalSize)
        self.normal_size_Act.setEnabled(False)



        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)


        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)


        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.revert_act)


        tool_menu = menu_bar.addMenu('Tools')
        tool_menu.addAction(self.crop_act)
        tool_menu.addAction(self.resize_act)
        tool_menu.addSeparator()
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)
        tool_menu.addSeparator()
        tool_menu.addAction(self.zoom_in_act)
        tool_menu.addAction(self.zoom_out_act)
        tool_menu.addAction(self.normal_size_Act)

    def createToolBar(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    #app.setStyleSheet(style_sheet)
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
