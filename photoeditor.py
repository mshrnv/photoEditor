from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QToolBar, QAction, QSlider, QGridLayout,
                             QWidget, QMainWindow, QLabel, QMessageBox,
                             QScrollArea, QDockWidget, QToolButton)
from PyQt5.QtGui import QImage, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize
from image import ImageLabel
import styles
import os

ICON_PATH = 'icons'

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
        self.image_label = ImageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = QScrollArea()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        
        self.scroll_area.setWidget(self.image_label)

        # Главный виджет
        self.setCentralWidget(self.scroll_area)

    def createEditingBar(self):
        """Создает меню редактирования"""

        # Инициализация меню редактирования
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(120)

        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setText('Черно-белый')
        convert_to_grayscale.setStyleSheet(styles.filter_button)
        #convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        #convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        convert_to_sepia = QToolButton()
        convert_to_sepia.setText('Сепия')
        convert_to_sepia.setStyleSheet(styles.filter_button)
        #convert_to_sepia.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        #convert_to_sepia.clicked.connect(self.image_label.convertToSepia)

        convert_to_negative = QToolButton()
        convert_to_negative.setText('Негатив')
        convert_to_negative .setStyleSheet(styles.filter_button)
        #change_hue.setIcon(QIcon(os.path.join(icon_path, "")))
        #change_hue.clicked.connect(self.image_label.changeHue)

        # Яркость изображения
        brightness_label = QLabel("Яркость")
        brightness_label.setStyleSheet(styles.edit_label)
        brightness_label.setAlignment(Qt.AlignCenter)
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-255, 255)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setPageStep(50)
        self.brightness_slider.setTickPosition(QSlider.TicksAbove)
        self.brightness_slider.setStyleSheet(styles.slider)
        #self.brightness_slider.valueChanged.connect(self.image_label.changeBrighteness)

        # Контраст изображения 
        contrast_label = QLabel("Контраст")
        contrast_label.setStyleSheet(styles.edit_label)
        contrast_label.setAlignment(Qt.AlignCenter)
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-255, 255)
        self.contrast_slider.setTickInterval(10)
        self.contrast_slider.setPageStep(50)
        self.contrast_slider.setTickPosition(QSlider.TicksAbove)
        self.contrast_slider.setStyleSheet(styles.slider)
        #self.contrast_slider.valueChanged.connect(self.image_label.changeContrast)

        # Сетка кнопок на панели редактирования
        editing_grid = QGridLayout()
        editing_grid.addWidget(convert_to_grayscale, 1, 0, 1, 0)
        editing_grid.addWidget(convert_to_sepia, 2, 0, 1, 0)
        editing_grid.addWidget(convert_to_negative, 3, 0, 1, 0)
        editing_grid.addWidget(brightness_label, 4, 0 , 1, 0)
        editing_grid.addWidget(self.brightness_slider, 5, 0, 1, 0)
        editing_grid.addWidget(contrast_label, 6, 0, 1, 0)
        editing_grid.addWidget(self.contrast_slider, 7, 0, 1, 0)
        editing_grid.setRowStretch(8, 10)

        # Инициализация виджета, используя сетку
        container = QWidget()
        container.setLayout(editing_grid)

        # Добавление меню к этому виджету
        self.editing_bar.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.editing_bar)
        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def createMenu(self):
        """Создает меню приложения"""

        # Actions для Photo Editor menu

        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About")
        about_dialog.setText("Какой-то текст.")
        about_dialog.setBaseSize(QSize(600, 120));

        about_act = QAction('About', self)
        about_act.triggered.connect(about_dialog.exec_)

        self.exit_act = QAction(QIcon(os.path.join(ICON_PATH, "exit.png")) ,'Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Actions для File menu

        self.open_act = QAction(QIcon(os.path.join(ICON_PATH, "open.png")) ,'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.image_label.openImage)

        self.save_act = QAction(QIcon(os.path.join(ICON_PATH, "save.png")) ,"Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        #self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions для Edit menu

        self.revert_act = QAction("Revert to Original", self)
        #self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions для Tools menu

        self.crop_act = QAction(QIcon(os.path.join(ICON_PATH, "selection.png")), "Crop", self)
        self.crop_act.setShortcut('Shift+X')
        #self.crop_act.triggered.connect(self.image_label.cropImage)
        self.crop_act.setEnabled(False)

        self.resize_act = QAction(QIcon(os.path.join(ICON_PATH, "move.png")), "Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        #self.resize_act.triggered.connect(self.image_label.resizeImage)
        self.resize_act.setEnabled(False)

        self.rotate90_cw_act = QAction(QIcon(os.path.join(ICON_PATH, "rotateccw.png")), 'Rotate ->', self)
        #self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage90("cw"))
        self.rotate90_cw_act.setEnabled(False)

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(ICON_PATH, "rotateccw.png")), 'Rotate <-', self)
        #self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage90("ccw"))
        self.rotate90_ccw_act.setEnabled(False)

        self.flip_horizontal = QAction(QIcon(os.path.join(ICON_PATH, "fliph.png")), 'Flip Horizontal', self)
        #self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))
        self.flip_horizontal.setEnabled(False)

        self.flip_vertical = QAction(QIcon(os.path.join(ICON_PATH, "flipv.png")), 'Flip Vertical', self)
        #self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        self.flip_vertical.setEnabled(False)
        
        self.zoom_in_act = QAction(QIcon(os.path.join(ICON_PATH, "zoom-in.png")), 'Zoom In', self)
        self.zoom_in_act.setShortcut('Ctrl++')
        #self.zoom_in_act.triggered.connect(lambda: self.zoomOnImage(1.25))
        self.zoom_in_act.setEnabled(False)

        self.zoom_out_act = QAction(QIcon(os.path.join(ICON_PATH, "zoom-out.png")), 'Zoom Out', self)
        self.zoom_out_act.setShortcut('Ctrl+-')
        #self.zoom_out_act.triggered.connect(lambda: self.zoomOnImage(0.8))
        self.zoom_out_act.setEnabled(False)

        self.normal_size_act = QAction("Normal Size", self)
        self.normal_size_act.setShortcut('Ctrl+=')
        #self.normal_size_act.triggered.connect(self.normalSize)
        self.normal_size_act.setEnabled(False)

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
        tool_menu.addAction(self.normal_size_act)

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