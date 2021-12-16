from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QColor, qRgb, QTransform
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance, ImageOps
import os
from shutil import copyfile

class ImageLabel(QLabel):
    """
    Класс используется для работы с лейблом изображения
    
    Основное применение - работа с изображением на экране (открытие, редактирование...).
    
    Attributes
    ----------
    image : QImage
        Изображение на экране
    parent : PhotoEditorGUI
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
    def __init__(self, parent, image = None):
        """Конструктор класса ImageLabel"""

        super().__init__(parent)

        # parent - родительский элемент, в котором содержится QImage
        self.parent = parent 
        self.image  = QImage()

        # Обнуляем значения слайдеров
        self.brightness = 0
        self.contrast   = 0

        # Вывод изображения на экран (по умолчанию - ничего)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

    def openImage(self):
        """Функция предлагает выбрать изображение и открывает его"""

        # Открытие QFileDialog для выбора изображения нужного расширения
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);JPG Files (*.jpeg *.jpg )")

        if image_file:

            # Путь к папке, где выполняется скрипт
            script_path = os.path.dirname(__file__)

            # Формирование пути к оригинальному изображению во временной папке и его копирование туда
            self.original_image_path = os.path.join(script_path, 'temp/original.png')
            copyfile(image_file, self.original_image_path)

            # Формирование пути к промежуточно-отредактированному изображению во временной папке и его копирование туда
            self.tmp_image_path = os.path.join(script_path, 'temp/temp.png')
            copyfile(image_file, self.tmp_image_path)

            # Устанавливаем выбранное изображение, как свойство класса
            self.image = QImage(image_file)

            # Отображение изображения на экране
            self.setPixmap(QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

            # Делаем кнопки редактирования доступными
            self.parent.updateActions()

            # Обнуляем значения слайдеров
            self.resetValues()


        elif image_file == '':

            # Пользватель выбрал 'Назад'
            pass
        else:

            # Какая-то другая ошибка
            pass

    def revertToOriginal(self):
        """Возвращает ищображение к оригинальному"""

        # Замена промежуточного файла на оригинальный (тот, который был при загрузке)
        copyfile(self.original_image_path, self.tmp_image_path)

        # Открываем его
        self.image = QImage(self.tmp_image_path)

        # Сбрасываем значения
        self.resetValues()

        # Показываем на экране
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

    def flipImage(self, axis):
        """Отражает изображение вдоль оси"""

        # Если на экране есть изображение
        if self.image.isNull() == False:

            # Если отразить по горизонтали то поворачиваем относительно OY
            if axis == 'horizontal':
                flip = QTransform().scale(1, -1)
            # Если отразить по вертикали то поворачиваем относительно OX
            elif axis == 'vertical':
                flip = QTransform().scale(-1, 1)

            # Формируем новое изображение
            pixmap = QPixmap(self.image)
            flipped = pixmap.transformed(flip)
            self.image = QImage(flipped)

            # Сохраняем его и заново открываем
            self.image.save(self.tmp_image_path)
            self.updateImage()
        else:
            # Ошибка, не загружена фотография
            pass

    def saveImage(self):
        """Сохраняет изображение"""

        # Окно выбора куда сохранять
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg )")

            # Если выбранный путь - корректный, то сохраняем туда файл
            if image_file:
                self.image.save(image_file)

    def rotateImage(self, direction):
        """Поворачивает изображение на 90 градусов"""

        # Если на экране есть изображение
        if self.image.isNull() == False:

            # Определяем направление поворота и поворачиваем изображение
            # CW  - По часовой
            # CCW - Против часовой
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            # Формируем новое изображение
            pixmap = QPixmap(self.image)
            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())
            self.image = QImage(rotated) 

            # Сохраняем и открываем его
            self.image.save(self.tmp_image_path)
            self.updateImage()

    def convertToSepia(self):
        """Накалдывает фильтр сепия"""

        # Если на экране есть изображение
        if self.image.isNull() == False:

            # Открываем временный файл
            img = Image.open(self.tmp_image_path)
            width, height = img.size

            # Получаем массив пикселей изображения
            pixels = img.load()

            # Начинаем пробегать по каждому пикселю изображения
            for py in range(height):
                for px in range(width):

                    # Обработка исключений на случай ошибки, чтобы не крашилось
                    try:
                        r, g, b = img.getpixel((px, py))
                    except Exception as e:
                        print(e)
                        return 1

                    # Вычисление RGB нового пикселя
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    if tr > 255:
                        tr = 255

                    if tg > 255:
                        tg = 255

                    if tb > 255:
                        tb = 255

                    # Замена пикселя на новый
                    pixels[px, py] = (tr,tg,tb)

            # Сохраняем изображение и открываем его
            img.save(self.tmp_image_path)
            self.updateImage()

    def convertToNegativ(self):
        """Накладывает фильтр негатив"""

        # Если на экране есть изображение
        if self.image.isNull() == False:

            # Открываем изображение, инвертируем пиксели и сохраняем
            im = Image.open(self.tmp_image_path)
            im_output = ImageOps.invert(im)
            im_output.save(self.tmp_image_path)

            # Открываем его на экране
            self.updateImage()

    def convertToGray(self):
        """Накладывате черно-белый фильтр"""

        # Если на экране есть изображение
        if self.image.isNull() == False:

            # Открываем изображение, применяем фильтр и сохраняем
            im = Image.open(self.tmp_image_path)
            im_output = ImageOps.grayscale(im)
            im_output.save(self.tmp_image_path)

            # Открываем его на экране
            self.updateImage()

    def changeBrighteness(self):
        """Изменяет яркость изображения"""

        # Вычисление значения насколько увеличилась яркость
        brightness      = self.parent.brightness_slider.value()
        diff            = brightness - self.brightness
        self.brightness = brightness

        factor = 1

        # Вычисление коэффицента увелчиения/уменьшения яркости
        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1

        # Открываем изображение, работаем с ярокстью, сохраняем его
        im = Image.open(self.tmp_image_path)
        enhancer = ImageEnhance.Brightness(im)
        im_output = enhancer.enhance(factor)
        im_output.save(self.tmp_image_path)

        # Открываем изображение и показываем его
        self.updateImage()

    def changeContrast(self):
        """Изменяет контраст изображения"""

        # Вычисление значения насколько увеличился контраст
        contrast      = self.parent.contrast_slider.value()
        diff          = contrast - self.contrast
        self.contrast = contrast

        factor = 1
        
        # Вычисление коэффицента увелчиения/уменьшения контраста
        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1

        # Открываем изображение, работаем с контрастом, сохраняем его
        im = Image.open(self.tmp_image_path)
        im_output = ImageEnhance.Contrast(im).enhance(factor)
        im_output.save(self.tmp_image_path)
        
        # Открываем изображение и показываем его
        self.updateImage()

    def updateImage(self):
        """Открывает промежуточное изображение и показывает его на экране"""

        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint

    def resetValues(self):
        """Обнуляет все значения слайдеров"""

        self.contrast   = 0
        self.brightness = 0
        self.parent.brightness_slider.setValue(0)
        self.parent.contrast_slider.setValue(0)