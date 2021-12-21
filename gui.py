"""
    Импорт стилей, функций шифрования, копирования файлов
    Импорт компонентов PyQt
"""
import os
from shutil import copyfile
from hashlib import sha256
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from image import ImageLabel
from database import DatabaseQuery
import styles

# Путь к папке с иконками
ICON_PATH = "icons"


class PhotoEditorGui(PyQt5.QtWidgets.QMainWindow):
    """
    Класс используется для работы с окном фоторедактора

    Основное применение - работа с UI окна фоторедактора.
    """

    def __init__(self, orig_path, temp_path, username):
        """
        Констрктор класса PhotoEditorGui

        Args:
            orig_path (String): Путь к оригинальному изображению
            temp_path (String): Путь к временному изображению
            username  (String): Логин пользователя
        """

        super().__init__()

        # Присваивание значений свойствам класса
        self.image = PyQt5.QtGui.QImage()
        self.username = username

        # Запуск окна и открытие изображения
        self.setup_ui()
        self.image_label.open_image(orig_path, temp_path)

    def setup_ui(self):
        """
        Главный метод, создающий окно и рисующий все компоненты
        """

        # Параметры окна
        self.setMinimumSize(300, 200)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "photoshop.png")))
        # self.showMaximized()
        self.resize(640, 480)

        # Отрисовка всех компонентов окна
        self.create_main_label()
        self.create_editing_bar()
        self.create_menu()
        self.create_tool_bar()

    def create_main_label(self):
        """
        Создает центральный(главный) виджет приложения
        """

        # Создание лейбла с изображением
        self.image_label = ImageLabel(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = PyQt5.QtWidgets.QScrollArea()
        self.scroll_area.setBackgroundRole(PyQt5.QtGui.QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_label)

        # Главный виджет
        self.setCentralWidget(self.scroll_area)

    def create_editing_bar(self):
        """
        Создает меню редактирования
        """

        # Инициализация меню редактирования
        self.editing_bar = PyQt5.QtWidgets.QDockWidget("Инструменты")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(120)
        self.editing_bar.setStyleSheet(styles.DOCK_WIDGET)

        # Кнопка с фильтром ЧБ
        convert_to_grayscale = PyQt5.QtWidgets.QToolButton()
        convert_to_grayscale.setText("Черно-белый")
        convert_to_grayscale.setStyleSheet(styles.FILTER_BUTTON)
        convert_to_grayscale.clicked.connect(self.image_label.convert_to_gray)

        # Кнопка с фильтром Сепия
        convert_to_sepia = PyQt5.QtWidgets.QToolButton()
        convert_to_sepia.setText("Сепия")
        convert_to_sepia.setStyleSheet(styles.FILTER_BUTTON)
        convert_to_sepia.clicked.connect(self.image_label.convert_to_sepia)

        # Кнопка с фильтром Негатив
        convert_to_negative = PyQt5.QtWidgets.QToolButton()
        convert_to_negative.setText("Негатив")
        convert_to_negative.setStyleSheet(styles.FILTER_BUTTON)
        convert_to_negative.clicked.connect(self.image_label.convert_to_negativ)

        # Яркость изображения

        # Надпись "Яркость"
        brightness_label = PyQt5.QtWidgets.QLabel("Яркость")
        brightness_label.setStyleSheet(styles.EDIT_LABEL)
        brightness_label.setAlignment(Qt.AlignCenter)

        # Слайдер яркости
        self.brightness_slider = PyQt5.QtWidgets.QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-5, 5)
        self.brightness_slider.setTickInterval(0)
        self.brightness_slider.setPageStep(0)
        self.brightness_slider.setTickPosition(PyQt5.QtWidgets.QSlider.TicksAbove)
        self.brightness_slider.setStyleSheet(styles.SLIDER)
        self.brightness_slider.sliderReleased.connect(
            self.image_label.change_brighteness
        )

        # Контраст изображения

        # Надпись "Контраст"
        contrast_label = PyQt5.QtWidgets.QLabel("Контраст")
        contrast_label.setStyleSheet(styles.EDIT_LABEL)
        contrast_label.setAlignment(Qt.AlignCenter)

        # Слайдер контраста
        self.contrast_slider = PyQt5.QtWidgets.QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(-5, 5)
        self.contrast_slider.setTickInterval(0)
        self.contrast_slider.setPageStep(0)
        self.contrast_slider.setTickPosition(PyQt5.QtWidgets.QSlider.TicksAbove)
        self.contrast_slider.setStyleSheet(styles.SLIDER)
        self.contrast_slider.sliderReleased.connect(
            self.image_label.change_contrast
        )

        # Сетка кнопок на панели редактирования
        editing_grid = PyQt5.QtWidgets.QGridLayout()
        editing_grid.addWidget(convert_to_grayscale, 1, 0, 1, 0)
        editing_grid.addWidget(convert_to_sepia, 2, 0, 1, 0)
        editing_grid.addWidget(convert_to_negative, 3, 0, 1, 0)
        editing_grid.addWidget(brightness_label, 4, 0, 1, 0)
        editing_grid.addWidget(self.brightness_slider, 5, 0, 1, 0)
        editing_grid.addWidget(contrast_label, 6, 0, 1, 0)
        editing_grid.addWidget(self.contrast_slider, 7, 0, 1, 0)
        editing_grid.setRowStretch(8, 10)

        # Инициализация виджета, используя сетку
        container = PyQt5.QtWidgets.QWidget()
        container.setLayout(editing_grid)

        # Добавление меню к этому виджету
        self.editing_bar.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.editing_bar)
        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def create_menu(self):
        """
        Создает меню приложения
        """

        # Actions для Photo Editor menu

        about_dialog = PyQt5.QtWidgets.QMessageBox(self)
        about_dialog.setWindowTitle("О программе")
        about_dialog.setText("Фоторедактор на PyQt5 и Pillow.")
        about_dialog.setBaseSize(PyQt5.QtCore.QSize(600, 120))

        about_act = PyQt5.QtWidgets.QAction("О программе...", self)
        about_act.triggered.connect(about_dialog.exec_)

        self.back_act = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "back.png")), "Назад", self
        )
        self.back_act.setShortcut("Ctrl+Q")
        self.back_act.triggered.connect(self.back_to_selection)

        # Actions для File menu

        self.save_act = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "save.png")), "Сохранить файл...", self
        )
        self.save_act.setShortcut("Ctrl+S")
        self.save_act.triggered.connect(self.image_label.save_image)
        self.save_act.setEnabled(False)

        # Actions для Edit menu

        self.revert_act = PyQt5.QtWidgets.QAction("Отменить редактирование", self)
        self.revert_act.triggered.connect(self.image_label.revert_to_original)
        self.revert_act.setEnabled(False)

        # Actions для Tools menu

        self.rotate90_cw_act = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "rotatecw.png")), "Повернуть по часовой", self
        )
        self.rotate90_cw_act.triggered.connect(
            lambda: self.image_label.rotate_image("cw")
        )
        self.rotate90_cw_act.setEnabled(False)

        self.rotate90_ccw_act = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "rotateccw.png")),
            "Повернуть против часовой",
            self,
        )
        self.rotate90_ccw_act.triggered.connect(
            lambda: self.image_label.rotate_image("ccw")
        )
        self.rotate90_ccw_act.setEnabled(False)

        self.flip_horizontal = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "fliph.png")), "Отразить по горизонтали", self
        )
        self.flip_horizontal.triggered.connect(
            lambda: self.image_label.flip_image("horizontal")
        )
        self.flip_horizontal.setEnabled(False)

        self.flip_vertical = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "flipv.png")), "Отразить по вертикали", self
        )
        self.flip_vertical.triggered.connect(
            lambda: self.image_label.flip_image("vertical")
        )
        self.flip_vertical.setEnabled(False)

        # Создание menubar

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        menu_bar.setStyleSheet(styles.MENU_BAR)

        # Добавление Actions к Photo Editor

        main_menu = menu_bar.addMenu("Фоторедактор")
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.back_act)

        # Добавление Actions к File

        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.save_act)

        # Добавление Actions к Edit

        edit_menu = menu_bar.addMenu("Редактировать")
        edit_menu.addAction(self.revert_act)

        # Добавление Actions к Tools

        tool_menu = menu_bar.addMenu("Инструменты")
        tool_menu.addAction(self.rotate90_cw_act)
        tool_menu.addAction(self.rotate90_ccw_act)
        tool_menu.addAction(self.flip_horizontal)
        tool_menu.addAction(self.flip_vertical)

    def create_tool_bar(self):
        """
        Создает панель редактирования
        """

        # Добавление панели управления на основе главного меню

        tool_bar = PyQt5.QtWidgets.QToolBar("Панель редактирования")
        tool_bar.setIconSize(PyQt5.QtCore.QSize(26, 26))
        tool_bar.setStyleSheet(styles.TOOL_BAR)
        self.addToolBar(tool_bar)

        # Добавление Actions к tool_bar

        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.back_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.rotate90_cw_act)
        tool_bar.addAction(self.rotate90_ccw_act)
        tool_bar.addAction(self.flip_horizontal)
        tool_bar.addAction(self.flip_vertical)

    def update_actions(self):
        """
        Делает кнопки редактирования активными
        """

        # Делаем кнопки активными
        self.rotate90_cw_act.setEnabled(True)
        self.rotate90_ccw_act.setEnabled(True)
        self.flip_horizontal.setEnabled(True)
        self.flip_vertical.setEnabled(True)
        self.save_act.setEnabled(True)
        self.revert_act.setEnabled(True)

    def back_to_selection(self):
        """
        Функция для возврата к списку изображений
        """

        # Получаем список изображений пользователя
        images = DatabaseQuery().get_user_images(self.username)

        # Закрываем текущее окно и открываем новое
        self.close()
        self.selection = SelectionGui(self.username, images)
        self.selection.show()


class AuthGui(PyQt5.QtWidgets.QMainWindow):
    """
    Класс используется для работы с окном авторизации

    Основное применение - работа с UI окна.
    """

    def __init__(self):
        """
        Констрктор класса AuthGui
        """

        # Отрисовка интерфейса
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Главный метод, создающий окно и рисующий все компоненты
        """

        # Устанавливаем размер, название и иконку окна
        self.setFixedSize(500, 300)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.create_central_widget()

    def create_central_widget(self):
        """
        Метод, инициализирующий все компоненты окна
        """

        # Инициализация главного виджета
        self.centralwidget = PyQt5.QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Войти"
        self.auth_button = QtWidgets.QPushButton(self.centralwidget)
        self.auth_button.setText("Войти")
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
        self.password_label = PyQt5.QtWidgets.QLabel(self.centralwidget)
        self.password_label.setText("Пароль")
        self.password_label.setGeometry(QtCore.QRect(200, 110, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.password_label.setFont(font)
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")

        # Надпись "Логин"
        self.login_label = PyQt5.QtWidgets.QLabel()
        self.login_label.setText("Логин")
        self.login_label.setGeometry(QtCore.QRect(210, 40, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.login_label.setFont(font)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setObjectName("login_label")

        # Grid widget (сетка)
        editing_grid = PyQt5.QtWidgets.QGridLayout()
        editing_grid.addWidget(self.login_label, 1, 0, 1, 0)
        editing_grid.addWidget(self.login_input, 2, 0, 1, 0)
        editing_grid.addWidget(self.password_label, 3, 0, 1, 0)
        editing_grid.addWidget(self.password_input, 4, 0, 1, 0)
        editing_grid.addWidget(self.auth_button, 5, 0, 1, 0)

        editing_grid.setRowStretch(6, 7)

        # Инициализация виджета, используя сетку
        container = PyQt5.QtWidgets.QWidget()
        container.setLayout(editing_grid)

        self.setCentralWidget(container)

    def auth(self):
        """
        Функция проверяет введенные данные и определяет дальнейшее действие
        """

        # Получение значений из полей ввода
        username = self.login_input.text()
        password = self.password_input.text()

        # Получение хэша
        hash = sha256(
            (username + (sha256(password.encode("utf-8")).hexdigest())).encode("utf-8")
        ).hexdigest()

        # Получение пароля из базы
        response = DatabaseQuery().get_user_password(username)

        # Проверка ответа из БД
        if response is not False:

            if hash == response:
                # Авторизация

                # Получение списка изображений пользователя
                images = DatabaseQuery().get_user_images(username)

                # Закрытие текущего окна и открытие нового
                self.close()
                self.selection = SelectionGui(username, images)
                self.selection.show()
            else:
                # Ошибка авторизации
                # QErrorMessage
                pass
        else:
            # Регистрация
            print(f"NEW USER: {username}")
            DatabaseQuery().registrate_user(username, hash)

            script_path = os.path.dirname(__file__)
            user_folder_path = os.path.join(script_path, f"images/{username}")
            os.mkdir(user_folder_path)

            self.close()
            self.selection = SelectionGui(username)
            self.selection.show()


class SelectionGui(PyQt5.QtWidgets.QMainWindow):
    """
    Класс используется для работы с окном выбора изображения

    Основное применение - работа с UI окна.
    """

    def __init__(self, username, images=[]):
        """
        Констрктор класса SelectionGui

        Args:
            username (String): Логин пользователя
            images   (List)  : Список изображений. По умолчанию - пустой.
        """

        # Устанавливаем переданные параметры в свойства класса
        self.images = images
        self.username = username

        # Запсук окна и отрисовка его интерфейса
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Главный метод, создающий окно и рисующий все компоненты
        """

        # Устанавливаем размер, название и иконку окна
        self.setFixedSize(540, 360)
        self.setWindowTitle("Фоторедактор")
        self.setWindowIcon(PyQt5.QtGui.QIcon(os.path.join(ICON_PATH, "photoshop.png")))

        # Отрисовка всех компонентов окна
        self.create_central_widget()

    def create_central_widget(self):
        """
        Функция, создающая все компоненты окна
        """

        # Центральный (главный) виджет окна
        self.centralwidget = PyQt5.QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)

        # Сетка с компонентами окна
        self.grid_layout_widget = PyQt5.QtWidgets.QWidget(self.centralwidget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(30, 30, 471, 271))
        self.grid_layout_widget.setObjectName("grid_layout_widget")
        self.grid_layout = PyQt5.QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")

        # Кнопка "Загрузить"
        self.load_button = QtWidgets.QPushButton(self.grid_layout_widget)
        self.load_button.setObjectName("load_button")
        self.load_button.setText("Загрузить")
        self.load_button.clicked.connect(self.load_image)
        self.grid_layout.addWidget(self.load_button, 3, 0, 1, 1)

        # Кнопка "Редактировать"
        self.edit_button = QtWidgets.QPushButton(self.grid_layout_widget)
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setText("Редактировать")
        self.edit_button.clicked.connect(self.edit_image)
        self.grid_layout.addWidget(self.edit_button, 1, 0, 1, 1)

        # Кнопка "Выйти"
        self.exit_button = QtWidgets.QPushButton(self.grid_layout_widget)
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Выйти")
        self.exit_button.clicked.connect(self.exit)
        self.grid_layout.addWidget(self.exit_button, 4, 0, 1, 1)

        # Элемент - список изображений
        self.list = QtWidgets.QListWidget(self.grid_layout_widget)
        self.list.setObjectName("list")

        # Добавление фотографий в список для отображения на экране
        for image in self.images:
            item = QtWidgets.QListWidgetItem()
            item.setText(image)
            self.list.addItem(item)

        self.grid_layout.addWidget(self.list, 0, 0, 1, 1)

        # Установка главного виджета
        self.setCentralWidget(self.centralwidget)

    def edit_image(self):
        """
        Функция предназначена для открытия окна фоторедактора
        """

        # Получаем выбранный элемент списка
        name = self.list.currentItem().text()

        # Формируем пути к изображению и его копии
        script_path = os.path.dirname(__file__)
        orig_path = os.path.join(script_path, f"images/{self.username}/temp-{name}")
        temp_path = os.path.join(script_path, f"images/{self.username}/{name}")

        # Закрываем текущее окно и открываем новое
        self.close()
        self.editor = PhotoEditorGui(orig_path, temp_path, self.username)
        self.editor.show()

    def load_image(self):
        """
        Функция предназначена для загрузки изображения в базу
        """

        # Открытие QFileDialog для выбора изображения нужного расширения
        image_file, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Image", "", "PNG Files (*.png);JPG Files (*.jpeg *.jpg )"
        )

        # Путь к папке, где выполняется скрипт
        script_path = os.path.dirname(__file__)

        # Имя выбранного файла
        name = os.path.basename(image_file)

        # Копируем файл (оригинал)
        original_image_path = os.path.join(
            script_path, f"images/{self.username}/temp-{name}"
        )
        copyfile(image_file, original_image_path)

        # Копируем файл (временный)
        tmp_image_path = os.path.join(script_path, f"images\\{self.username}\\{name}")
        copyfile(image_file, tmp_image_path)

        # Добавляем новый элемент к списку
        item = QtWidgets.QListWidgetItem()
        item.setText(name)
        self.list.addItem(name)

        # Запись в БД
        DatabaseQuery().add_image(self.username, name)

    def exit(self):
        """
        Функция предназначена для выхода из сессии пользователя
        """

        # Закрываем текущее окно и открываем другое
        self.close()
        self.auth = AuthGui()
        self.auth.show()
