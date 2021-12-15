from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QColor, qRgb
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
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
    original_image : QImage
        Оригинальное изображение
    parent : PhotoEditorGUI
        Окно приложения
    """
    def __init__(self, parent, image = None):
        """Конструктор класса ImageLabel"""

        super().__init__(parent)

        # parent - родительский элемент, в котором содержится QImage
        self.parent = parent 
        self.image  = QImage()

        # Вывод изображения на экран (по умолчанию - ничего)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

    def openImage(self):
        """Функция предлагает выбрать изображение и открывает его"""

        # Открытие QFileDialog для выбора изображения нужного расширения
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", 
                "", "PNG Files (*.png);JPG Files (*.jpeg *.jpg )")

        if image_file:

            script_path = os.path.dirname(__file__)

            self.original_image_path = os.path.join(script_path, 'temp/original.png')
            copyfile(image_file, self.original_image_path)

            self.tmp_image_path = os.path.join(script_path, 'temp/temp.png')
            copyfile(image_file, self.tmp_image_path)

            self.image_path = self.tmp_image_path

            # Сбрасываем значения
            self.parent.zoom_factor = 1
            self.brightness = 0
            self.contrast   = 0

            # TODO: здесь нужно сбросить все кнопки и слайдеры

            # Устанавливаем выбранное изображение, как свойство класса
            self.image = QImage(image_file)

            # Это копия изображения (оригинал)
            self.original_image = self.image.copy()

            # Отображение изображения на экране
            self.setPixmap(QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

            self.parent.updateActions()

        elif image_file == '':

            # Пользватель выбрал 'Назад'
            pass
        else:

            # Какая-то другая ошибка
            pass

    def revertToOriginal(self):
        self.image = self.original_image.copy()
        self.contrast   = 0
        self.brightness = 0
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

    def saveImage(self):
        # Окно выбора куда сохранять
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg )")

            if image_file:
                self.image.save(image_file)

    def convertToSepia(self):
        if self.image.isNull() == False:

            img = Image.open(self.tmp_image_path)
            width, height = img.size

            pixels = img.load() # create the pixel map

            for py in range(height):
                for px in range(width):
                    r, g, b = img.getpixel((px, py))

                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    if tr > 255:
                        tr = 255

                    if tg > 255:
                        tg = 255

                    if tb > 255:
                        tb = 255

                    pixels[px, py] = (tr,tg,tb)
            img.save(self.tmp_image_path)

        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint

    def convertToNegativ(self):
        if self.image.isNull() == False:
            self.image.invertPixels()
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()

    def convertToGray(self):
        if self.image.isNull() == False:
            grayscale_img = self.image.convertToFormat(QImage.Format_Grayscale16)
            self.image = QImage(grayscale_img)
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint

    def changeBrighteness(self):
        brightness = self.parent.brightness_slider.value()
        diff = brightness - self.brightness
        factor = 1
        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1
        self.brightness = brightness

        im = Image.open(self.tmp_image_path)

        enhancer = ImageEnhance.Brightness(im)

        im_output = enhancer.enhance(factor)
        im_output.save(self.tmp_image_path)

        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint

    def changeContrast(self):
        contrast = self.parent.contrast_slider.value()
        diff = contrast - self.contrast
        factor = 1
        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1
        self.contrast = contrast

        image = Image.open(self.tmp_image_path)
        image = ImageEnhance.Contrast(image).enhance(factor)
        image.save(self.tmp_image_path)
        
        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint
