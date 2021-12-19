from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QToolBar, QAction, QSlider, QGridLayout,
                             QWidget, QMainWindow, QLabel, QMessageBox,
                             QScrollArea, QDockWidget, QToolButton)
from PyQt5.QtGui import QImage, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize
from image import ImageLabel
import styles
import os
from selection import SelectionGui

# Путь к папке с иконками
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
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH, "photoshop.png")))
        #self.showMaximized()
        self.resize(640, 480)

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
        self.editing_bar = QDockWidget("Инструменты")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(120)
        self.editing_bar.setStyleSheet(styles.dock_widget)

        # Кнопка с фильтром ЧБ
        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setText('Черно-белый')
        convert_to_grayscale.setStyleSheet(styles.filter_button)
        #convert_to_grayscale.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        # Кнопка с фильтром Сепия
        convert_to_sepia = QToolButton()
        convert_to_sepia.setText('Сепия')
        convert_to_sepia.setStyleSheet(styles.filter_button)
        #convert_to_sepia.setIcon(QIcon(os.path.join(icon_path, "ICON HERE")))
        convert_to_sepia.clicked.connect(self.image_label.convertToSepia)

        # Кнопка с фильтром Негатив
        convert_to_negative = QToolButton()
        convert_to_negative.setText('Негатив')
        convert_to_negative .setStyleSheet(styles.filter_button)
        #convert_to_negative.setIcon(QIcon(os.path.join(icon_path, "")))
        convert_to_negative.clicked.connect(self.image_label.convertToNegativ)

        # Яркость изображения
        brightness_label = QLabel("Яркость")
        brightness_label.setStyleSheet(styles.edit_label)
        brightness_label.setAlignment(Qt.AlignCenter)
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-5, 5)
        self.brightness_slider.setTickInterval(0)
        self.brightness_slider.setPageStep(0)
        self.brightness_slider.setTickPosition(QSlider.TicksAbove)
        self.brightness_slider.setStyleSheet(styles.slider)
        self.brightness_slider.sliderReleased.connect(self.image_label.changeBrighteness)

        # Контраст изображения 
        contrast_label = QLabel("Контраст")
        contrast_label.setStyleSheet(styles.edit_label)
        contrast_label.setAlignment(Qt.AlignCenter)
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-5, 5)
        self.contrast_slider.setTickInterval(0)
        self.contrast_slider.setPageStep(0)
        self.contrast_slider.setTickPosition(QSlider.TicksAbove)
        self.contrast_slider.setStyleSheet(styles.slider)
        self.contrast_slider.sliderReleased.connect(self.image_label.changeContrast)

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
        about_dialog.setWindowTitle("О программе")
        about_dialog.setText("Фоторедактор на PyQt5 и Pillow.")
        about_dialog.setBaseSize(QSize(600, 120));

        about_act = QAction('О программе...', self)
        about_act.triggered.connect(about_dialog.exec_)

        self.exit_act = QAction(QIcon(os.path.join(ICON_PATH, "exit.png")) ,'Выход', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Actions для File menu

        self.open_act = QAction(QIcon(os.path.join(ICON_PATH, "open.png")) ,'Открыть файл...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.image_label.openImage)

        self.save_act = QAction(QIcon(os.path.join(ICON_PATH, "save.png")) ,"Сохранить файл...", self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.image_label.saveImage)
        self.save_act.setEnabled(False)

        # Actions для Edit menu

        self.revert_act = QAction("Отменить редактирование", self)
        self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions для Tools menu

        self.rotate90_cw_act = QAction(QIcon(os.path.join(ICON_PATH, "rotatecw.png")), 'Повернуть по часовой', self)
        self.rotate90_cw_act.triggered.connect(lambda: self.image_label.rotateImage("cw"))
        self.rotate90_cw_act.setEnabled(False)

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(ICON_PATH, "rotateccw.png")), 'Повернуть против часовой', self)
        self.rotate90_ccw_act.triggered.connect(lambda: self.image_label.rotateImage("ccw"))
        self.rotate90_ccw_act.setEnabled(False)

        self.flip_horizontal = QAction(QIcon(os.path.join(ICON_PATH, "fliph.png")), 'Отразить по горизонтали', self)
        self.flip_horizontal.triggered.connect(lambda: self.image_label.flipImage("horizontal"))
        self.flip_horizontal.setEnabled(False)

        self.flip_vertical = QAction(QIcon(os.path.join(ICON_PATH, "flipv.png")), 'Отразить по вертикали', self)
        self.flip_vertical.triggered.connect(lambda: self.image_label.flipImage('vertical'))
        self.flip_vertical.setEnabled(False)

        # Создание menubar

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        menu_bar.setStyleSheet(styles.menu_bar)

        # Добавление Actions к Photo Editor

        main_menu = menu_bar.addMenu('Фоторедактор')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        # Добавление Actions к File

        file_menu = menu_bar.addMenu('Файл')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)

        # Добавление Actions к Edit

        edit_menu = menu_bar.addMenu('Редактировать')
        edit_menu.addAction(self.revert_act)

        # Добавление Actions к Tools

        tool_menu = menu_bar.addMenu('Инструменты')
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)

    def createToolBar(self):
        """Создает панель редактирования"""

        # Добавление панели управления на основе главного меню

        tool_bar = QToolBar('Панель редактирования')
        tool_bar.setIconSize(QSize(26, 26))
        tool_bar.setStyleSheet(styles.tool_bar)
        self.addToolBar(tool_bar)

        # Добавление Actions к tool_bar

        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.exit_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)

    def updateActions(self):

        # Делаем кнопки активными
        self.rotate90_cw_act.setEnabled(True)
        self.rotate90_ccw_act.setEnabled(True)
        self.flip_horizontal.setEnabled(True)
        self.flip_vertical.setEnabled(True)
        self.save_act.setEnabled(True)
        self.revert_act.setEnabled(True)