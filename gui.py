from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QToolBar, QAction, QSlider, QGridLayout,
                             QWidget, QMainWindow, QLabel, QMessageBox,
                             QScrollArea, QDockWidget, QToolButton, QFileDialog)
from PyQt5.QtGui import QImage, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize
from image import ImageLabel
import styles
import os
from database import DatabaseQuery
from shutil import copyfile

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
        # self.show()

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

        self.back_act = QAction(QIcon(os.path.join(ICON_PATH, "back.png")) ,'Назад', self)
        self.back_act.setShortcut('Ctrl+Q')
        self.back_act.triggered.connect(self.backToSelection)

        # Actions для File menu

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
        main_menu.addAction(self.back_act)

        # Добавление Actions к File

        file_menu = menu_bar.addMenu('Файл')
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

        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.back_act)
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

    def backToSelection(self):
        # Возврат к списку изображений
        pass
    
class AuthGui(QMainWindow):
    """Класс используется для работы с окном авторизации пользователей"""

    def __init__(self):
        """Констрктор класса AuthGui"""

        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Главный метод, создающий окно и рисующий все компоненты"""

        self.setFixedSize(500, 300)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.createCentralWidget()

        # Показ окна
        # self.show()

    def createCentralWidget(self):
        """Метод, инициализирующий все компоненты окна"""
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Войти"
        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setText('Войти')
        self.auth_button.setGeometry(QtCore.QRect(190, 210, 131, 51))
        self.auth_button.clicked.connect(self.auth)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.auth_button.setFont(font)
        self.auth_button.setAutoFillBackground(False)
        self.auth_button.setCheckable(False)
        self.auth_button.setObjectName("auth_button")

        # Поле ввода логина
        self.login_input = QtWidgets.QLineEdit(self.centralwidget)
        self.login_input.setGeometry(QtCore.QRect(140, 70, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.login_input.setFont(font)
        self.login_input.setText("")
        self.login_input.setAlignment(QtCore.Qt.AlignCenter)
        self.login_input.setObjectName("login_input")

        # Поле ввода пароля
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(140, 150, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_input.setFont(font)
        self.password_input.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.password_input.setText("")
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setObjectName("password_input")

        # Надпись "Пароль"
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setText('Пароль')
        self.password_label.setGeometry(QtCore.QRect(200, 110, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")

        # Надпись "Логин"
        self.login_label = QtWidgets.QLabel()
        self.login_label.setText('Логин')
        self.login_label.setGeometry(QtCore.QRect(210, 40, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.login_label.setFont(font)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setObjectName("login_label")
        
        # Grid widget (сетка)
        editing_grid = QGridLayout()
        editing_grid.addWidget(self.login_label, 1, 0, 1, 0)
        editing_grid.addWidget(self.login_input, 2, 0, 1, 0)
        editing_grid.addWidget(self.password_label, 3, 0, 1, 0)
        editing_grid.addWidget(self.password_input, 4, 0, 1, 0)
        editing_grid.addWidget(self.auth_button, 5, 0, 1, 0)

        editing_grid.setRowStretch(6, 7)

        # Инициализация виджета, используя сетку
        container = QWidget()
        container.setLayout(editing_grid)

        self.setCentralWidget(container)
    
    def auth(self):
        """Функция проверяет введенные данные и определяет дальнейшее действие"""
        
        username = self.login_input.text()
        password = self.password_input.text()
        
        response = DatabaseQuery().getUserPassword(username)
        
        if response != False:
            if (password == response):
                print('SUCCESS AUTH')
                images = DatabaseQuery().getUserImages(username)
                self.close()
                self.selection = SelectionGui(username, images)
                self.selection.show()
            else:
                print('FAIL AUTH')
                # QErrorMessage
        else:
            print(f"NEW USER: {username}")
            DatabaseQuery().registrateUser(username, password)
            # mkdir
            self.close()
            self.selection = SelectionGui(username)
            self.selection.show()
            
class SelectionGui(QMainWindow):
    """Класс используется для работы с окном выбора изображения"""

    def __init__(self, username, images = list()):
        """Констрктор класса SelectionGui"""

        self.images   = images
        self.username = username
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """Главный метод, создающий окно и рисующий все компоненты"""

        self.setFixedSize(540, 360)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.createCentralWidget()

        # Показ окна
        # self.show()

    def createCentralWidget(self):
        """Функция, создающая все компоненты окна"""

        # Центральный (главный) виджет окна
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)

        # Сетка с компонентами окна
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 471, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        # Кнопка "Загрузить"
        self.load_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.load_button.setObjectName("load_button")
        self.load_button.setText("Загрузить")
        self.load_button.clicked.connect(self.loadImage)
        self.gridLayout.addWidget(self.load_button, 3, 0, 1, 1)

        # Кнопка "Редактировать"
        self.edit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setText("Редактировать")
        self.edit_button.clicked.connect(self.editImage)
        self.gridLayout.addWidget(self.edit_button, 1, 0, 1, 1)

        # Кнопка "Выйти"
        self.exit_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Выйти")
        self.exit_button.clicked.connect(self.exit)
        self.gridLayout.addWidget(self.exit_button, 4, 0, 1, 1)

        # Элемент - список изображений
        self.list = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.list.setObjectName("list")
        
        # Добавление фотографий в список для отображения на экране
        for image in self.images:
            item = QtWidgets.QListWidgetItem()
            item.setText(image)
            self.list.addItem(item)

        self.gridLayout.addWidget(self.list, 0, 0, 1, 1)

        # Установка главного виджета
        self.setCentralWidget(self.centralwidget)

    def editImage(self):
        """Функция предназначена для открытия окна фоторедактора"""
        # Здеь будет открываться окно редактирования
        print('Редактирование')
        pass

    def loadImage(self):
        """Функция предназначена для загрузки изображения в базу"""
        
        # Открытие QFileDialog для выбора изображения нужного расширения
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);JPG Files (*.jpeg *.jpg )")
        print(image_file)
        # Путь к папке, где выполняется скрипт
        script_path = os.path.dirname(__file__)
        name = os.path.basename(image_file)
        print(name)
        original_image_path = os.path.join(script_path, f'images/{self.username}/temp-{name}')
        copyfile(image_file, original_image_path)

        # Формирование пути к промежуточно-отредактированному изображению во временной папке и его копирование туда
        tmp_image_path = os.path.join(script_path, f'images\\{self.username}\\{name}')
        copyfile(image_file, tmp_image_path)
        
        # Запись в БД
        DatabaseQuery().addImage(self.username, name)
        print('Загрузка')
        pass

    def exit(self):
        """Функция предназначена для выхода из сессии пользователя"""
        self.close()
        self.auth = AuthGui()
        self.auth.show()
        print('Выход')