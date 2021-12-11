"""Summary
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QToolBar, QAction, QSlider, QGridLayout,
                             QWidget, QApplication, QMainWindow,
                             QFileDialog, QLabel, QSizePolicy,
                             QScrollArea, QDockWidget, QToolButton)
from PyQt5.QtGui import QPixmap, QImage, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize

class imageLabel(QLabel):
    """
    Класс используется для работы с лейблом изображения
    
    Основное применение - работа с изображением на экране (открытие, редактирование...).
    
    Attributes
    ----------
    image : QImage
        Изображение на экране
    parent : PhotoEditorGUI
        Окно приложения
    """
    def __init__(self, parent, image=None):
        """Конструктор класса imageLabel"""

        super().__init__(parent)

        # parent - родительский элемент, в котором содержится QImage
        self.parent = parent 
        self.image = QImage()

        # Вывод изображения на экран (по умолчанию - ничего)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

class PhotoEditorGUI(QMainWindow):

    """
    Класс используется для работы с окном приложения
    
    Основное применение - работа с UI приложения.
    """
    
    def __init__(self):
        """Констрктор класса PhotoEditorGUI"""
        super().__init__()

        self.initializeUI()
        self.image = QImage()

    def initializeUI(self):
        """Главный метод, создающий окно и рисующий все компоненты"""

        # Параметры окна
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Photo Editor")
        #self.showMaximized()
        self.resize(640, 480)

        # Zoom изображения
        self.zoom_factor = 1

        # Отрисовка всех компонентов окна
        self.createMainLabel()
        self.createEditingBar()
        self.createMenu()
        self.createToolBar()

        # Показ окна
        self.show()

    def createMainLabel(self):
        """Создает центральный(главный) виджет приложения"""

        # Создание лейбла с изображением
        self.image_label = imageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        
        self.scroll_area.setWidget(self.image_label)

        # Главный виджет
        self.setCentralWidget(self.scroll_area)

    def createEditingBar(self):
        """Создает менюшку редактирования"""
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

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
        #change_hue.setIcon(QIcon(os.path.join(icon_path, "")))
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
        """Создает меню приложения"""

        # Actions для Photo Editor menu

        about_act = QAction('About', self)
        #about_act.triggered.connect(self.aboutDialog)

        self.exit_act = QAction('Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        #self.exit_act.triggered.connect(self.close)

        # Actions для File menu

        self.new_act = QAction('New...')

        self.open_act = QAction('Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        #self.open_act.triggered.connect(self.image_label.openImage)

        self.save_act = QAction("Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        #self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions для Edit menu

        self.revert_act = QAction("Revert to Original", self)
        #self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions для Tools menu

        self.crop_act = QAction("Crop", self)
        self.crop_act.setShortcut('Shift+X')
        #self.crop_act.triggered.connect(self.image_label.cropImage)

        self.resize_act = QAction("Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        #self.resize_act.triggered.connect(self.image_label.resizeImage)

        self.rotate90_cw_act = QAction('Rotate ->', self)
        #self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))

        self.rotate90_ccw_act = QAction('Rotate <-', self)
        #self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))

        self.flip_horizontal = QAction('Flip Horizontal', self)
        #self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))

        self.flip_vertical = QAction('Flip Vertical', self)
        #self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        
        self.zoom_in_act = QAction('Zoom In', self)
        self.zoom_in_act.setShortcut('Ctrl++')
        #self.zoom_in_act.triggered.connect(lambda: self.zoomOnImage(1.25))
        self.zoom_in_act.setEnabled(False)

        self.zoom_out_act = QAction('Zoom Out', self)
        self.zoom_out_act.setShortcut('Ctrl+-')
        #self.zoom_out_act.triggered.connect(lambda: self.zoomOnImage(0.8))
        self.zoom_out_act.setEnabled(False)

        self.normal_size_Act = QAction("Normal Size", self)
        self.normal_size_Act.setShortcut('Ctrl+=')
        #self.normal_size_Act.triggered.connect(self.normalSize)
        self.normal_size_Act.setEnabled(False)

        # Создание menubar

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Добавление Actions к Photo Editor

        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        # Добавление Actions к File

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)

        # Добавление Actions к Edit

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.revert_act)

        # Добавление Actions к Tools

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
        """Создает панель редактирования"""

        # Добавление панели управления на основе главного меню

        tool_bar = QToolBar('Main Toolbar')
        tool_bar.setIconSize(QSize(26, 26))
        self.addToolBar(tool_bar)

        # Добавление Actions к tool_bar

        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.crop_act)
        tool_bar.addAction(self.resize_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)
        tool_bar.addSeparator()
        tool_bar.addAction(self.zoom_in_act)
        tool_bar.addAction(self.zoom_out_act)

if __name__ == "__main__":

    # Создание приложения QT
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    # Инициализация окна фоторедактора и его отображение
    window = PhotoEditorGUI()
    sys.exit(app.exec_())
