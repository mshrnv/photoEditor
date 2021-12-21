"""
    Импорт PyQt, Pillow и функции копирования файлов
"""
from shutil import copyfile
from PIL import Image, ImageEnhance, ImageOps
import PyQt5

class ImageLabel(PyQt5.QtWidgets.QLabel):
    """
    Класс используется для работы с лейблом изображения

    Основное применение - работа с изображением на экране (открытие, редактирование...).

    Attributes
    ----------
    image : QImage
        Изображение на экране
    parent : PhotoEditorGui
        Окно приложения
    original_image_path: String
        Путь оригинальному изображению во временной папке
    tmp_image_path : String
        Путь к промежуточно отредактированному изображению во временной папке
    brightness : Integer
        Текущее значение слайдера яркости
    contrast : Integer
        Текущее значение слайдера контраста
    """

    def __init__(self, parent):
        """
        Конструктор класса ImageLabel

        Args:
            parent (PhotoEditorGui): Родительское окно (окно фоторедактора)
        """

        super().__init__(parent)

        # parent - родительский элемент, в котором содержится QImage
        self.parent = parent
        self.image = PyQt5.QtGui.QImage()

        # Обнуляем значения слайдеров
        self.brightness = 0
        self.contrast = 0

        # Инициализируем свойства
        self.original_image_path = ''
        self.tmp_image_path = ''

        # Вывод изображения на экран (по умолчанию - ничего)
        self.setPixmap(PyQt5.QtGui.QPixmap().fromImage(self.image))
        self.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

    def open_image(self, orig_path, temp_path):
        """
        Функция предлагает выбрать изображение и открывает его

        Args:
            orig_path (String): Путь к оригинальному изображению
            temp_path (String): Путь к временному изображению
        """

        if orig_path and temp_path:

            # Присваивание значений свойствам
            self.original_image_path = orig_path
            self.tmp_image_path = temp_path

            # Устанавливаем выбранное изображение, как свойство класса
            self.image = PyQt5.QtGui.QImage(self.tmp_image_path)

            # Отображение изображения на экране
            self.setPixmap(PyQt5.QtGui.QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

            # Делаем кнопки редактирования доступными
            self.parent.updateActions()

            # Обнуляем значения слайдеров
            self.reset_values()

    def revert_to_original(self):
        """
        Возвращает ищображение к оригинальному
        """

        # Замена промежуточного файла на оригинальный (тот, который был при загрузке)
        copyfile(self.original_image_path, self.tmp_image_path)

        # Сбрасываем значения
        self.reset_values()

        # Показываем на экране
        self.update_image()

    def flip_image(self, axis):
        """
        Отражает изображение вдоль оси

        Args:
            axis (String): Ось, вдоль которой отразить
        """

        # Если на экране есть изображение
        if self.image.isNull() is False:

            # Если отразить по горизонтали то поворачиваем относительно OY
            if axis == "horizontal":
                flip = PyQt5.QtGui.QTransform().scale(1, -1)
            # Если отразить по вертикали то поворачиваем относительно OX
            elif axis == "vertical":
                flip = PyQt5.QtGui.QTransform().scale(-1, 1)

            # Формируем новое изображение
            pixmap = PyQt5.QtGui.QPixmap(self.image)
            flipped = pixmap.transformed(flip)
            self.image = PyQt5.QtGui.QImage(flipped)

            # Сохраняем его и заново открываем
            self.image.save(self.tmp_image_path)
            self.update_image()
        else:
            # Ошибка, не загружена фотография
            pass

    def save_image(self):
        """
        Сохраняет изображение
        """

        # Окно выбора куда сохранять
        if self.image.isNull() is False:
            image_file, _ = PyQt5.QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg )"
            )

            # Если выбранный путь - корректный, то сохраняем туда файл
            if image_file:
                self.image.save(image_file)

    def rotate_image(self, direction):
        """
        Поворачивает изображение на 90 градусов

        Args:
            direction (String): Направление поворота на 90 градусов
                CW  - По часовой
                CCW - Против часовой
        """

        # Если на экране есть изображение
        if self.image.isNull() is False:

            # Определяем направление поворота и поворачиваем изображение
            if direction == "cw":
                transform90 = PyQt5.QtGui.QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = PyQt5.QtGui.QTransform().rotate(-90)

            # Формируем новое изображение
            pixmap = PyQt5.QtGui.QPixmap(self.image)
            rotated = pixmap.transformed(transform90, mode=PyQt5.QtCore.Qt.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())
            self.image = PyQt5.QtGui.QImage(rotated)

            # Сохраняем и открываем его
            self.image.save(self.tmp_image_path)
            self.update_image()

    def convert_to_sepia(self):
        """
        Накалдывает фильтр сепия
        """

        # Если на экране есть изображение
        if self.image.isNull() is False:

            # Открываем временный файл
            img = Image.open(self.tmp_image_path)
            width, height = img.size

            # Получаем массив пикселей изображения
            pixels = img.load()

            # Начинаем пробегать по каждому пикселю изображения
            for pixel_y in range(height):
                for pixel_x in range(width):

                    # Обработка исключений на случай ошибки, чтобы не крашилось
                    try:
                        red, green, blue = img.getpixel((pixel_x, pixel_y))
                    except TypeError as error:
                        print(error)
                        return 1

                    # Вычисление RGB нового пикселя
                    new_red   = int(0.393 * red + 0.769 * green + 0.189 * blue)
                    new_green = int(0.349 * red + 0.686 * green + 0.168 * blue)
                    new_blue  = int(0.272 * red + 0.534 * green + 0.131 * blue)

                    new_red   = min(new_red, 255)
                    new_green = min(new_green, 255)
                    new_blue  = min(new_blue, 255)

                    # Замена пикселя на новый
                    pixels[pixel_x, pixel_y] = (new_red, new_green, new_blue)

            # Сохраняем изображение и открываем его
            img.save(self.tmp_image_path)
            self.update_image()

    def convert_to_negativ(self):
        """
        Накладывает фильтр негатив
        """

        # Если на экране есть изображение
        if self.image.isNull() is False:

            # Открываем изображение, инвертируем пиксели и сохраняем
            image = Image.open(self.tmp_image_path)
            image_output = ImageOps.invert(image)
            image_output.save(self.tmp_image_path)

            # Открываем его на экране
            self.update_image()

    def convert_to_gray(self):
        """
        Накладывате черно-белый фильтр
        """

        # Если на экране есть изображение
        if self.image.isNull() is False:

            # Открываем изображение, применяем фильтр и сохраняем
            image = Image.open(self.tmp_image_path)
            image_output = ImageOps.grayscale(image)
            image_output.save(self.tmp_image_path)

            # Открываем его на экране
            self.update_image()

    def change_brighteness(self):
        """
        Изменяет яркость изображения
        """

        # Если не открыто изображение - ничего не редактируем
        if self.image.isNull() is True:
            return 1

        # Вычисление значения насколько увеличилась яркость
        brightness = self.parent.brightness_slider.value()
        diff = brightness - self.brightness
        self.brightness = brightness

        factor = 1

        # Вычисление коэффицента увелчиения/уменьшения яркости
        if diff > 0:
            factor = pow(1.1, diff)
        elif diff < 0:
            factor = 1 + diff * 0.05

        # Открываем изображение, работаем с ярокстью, сохраняем его
        image = Image.open(self.tmp_image_path)
        image_output = ImageEnhance.Brightness(image).enhance(factor)
        image_output.save(self.tmp_image_path)

        # Открываем изображение и показываем его
        self.update_image()

    def change_contrast(self):
        """
        Изменяет контраст изображения
        """

        # Если не открыто изображение - ничего не редактируем
        if self.image.isNull() is True:
            return 1

        # Вычисление значения насколько увеличился контраст
        contrast = self.parent.contrast_slider.value()
        diff = contrast - self.contrast
        self.contrast = contrast

        factor = 1

        # Вычисление коэффицента увелчиения/уменьшения контраста
        if diff > 0:
            factor = pow(1.1, diff)
        elif diff < 0:
            factor = 1 + diff * 0.05

        # Открываем изображение, работаем с контрастом, сохраняем его
        image = Image.open(self.tmp_image_path)
        image_output = ImageEnhance.Contrast(image).enhance(factor)
        image_output.save(self.tmp_image_path)

        # Открываем изображение и показываем его
        self.update_image()

    def update_image(self):
        """
        Открывает промежуточное изображение и показывает его на экране
        """

        # Открытие и отображение файла на экране
        self.image = PyQt5.QtGui.QImage(self.tmp_image_path)
        self.setPixmap(PyQt5.QtGui.QPixmap().fromImage(self.image))
        self.repaint()

    def reset_values(self):
        """
        Обнуляет все значения слайдеров
        """

        self.contrast = 0
        self.brightness = 0
        self.parent.brightness_slider.setValue(0)
        self.parent.contrast_slider.setValue(0)
