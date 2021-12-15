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
            self.brightness = 0
            self.contrast   = 0

            # TODO: здесь нужно сбросить все кнопки и слайдеры

            # Устанавливаем выбранное изображение, как свойство класса
            self.image = QImage(image_file)

            # Отображение изображения на экране
            self.setPixmap(QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

            self.parent.updateActions()
            self.parent.brightness_slider.setValue(0)
            self.parent.contrast_slider.setValue(0)

        elif image_file == '':

            # Пользватель выбрал 'Назад'
            pass
        else:

            # Какая-то другая ошибка
            pass

    def revertToOriginal(self):
        copyfile(self.original_image_path, self.tmp_image_path)
        self.image = QImage(self.tmp_image_path)
        self.contrast   = 0
        self.brightness = 0
        self.parent.brightness_slider.setValue(0)
        self.parent.contrast_slider.setValue(0)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

    def flipImage(self, axis):
        if self.image.isNull() == False:
            if axis == 'horizontal':
                flip = QTransform().scale(1, -1)
            elif axis == 'vertical':
                flip = QTransform().scale(-1, 1)

            pixmap = QPixmap(self.image)
            flipped = pixmap.transformed(flip)
            self.image = QImage(flipped)

            self.image.save(self.tmp_image_path)
            self.image = QImage(self.tmp_image_path)
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint
        else:
            # Ошибка, не загружена фотография
            pass

    def saveImage(self):
        # Окно выбора куда сохранять
        if self.image.isNull() == False:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg )")

            if image_file:
                self.image.save(image_file)

    def rotateImage(self, direction):
        if self.image.isNull() == False:
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())

            self.image = QImage(rotated) 

            self.image.save(self.tmp_image_path)
            self.image = QImage(self.tmp_image_path)
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint

    def convertToSepia(self):
        if self.image.isNull() == False:

            img = Image.open(self.tmp_image_path)
            width, height = img.size

            pixels = img.load() # create the pixel map

            for py in range(height):
                for px in range(width):
                    try:
                        r, g, b = img.getpixel((px, py))
                    except Exception as e:
                        print(e)
                        return 1

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
            im = Image.open(self.tmp_image_path)
            im_output = ImageOps.invert(im)
            im_output.save(self.tmp_image_path)

            self.image = QImage(self.tmp_image_path)
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()

    def convertToGray(self):
        if self.image.isNull() == False:
            im = Image.open(self.tmp_image_path)
            im_output = ImageOps.grayscale(im)
            im_output.save(self.tmp_image_path)

            self.image = QImage(self.tmp_image_path)
            self.setPixmap(QPixmap().fromImage(self.image))
            self.repaint()

    def changeBrighteness(self):
        brightness      = self.parent.brightness_slider.value()
        diff            = brightness - self.brightness
        self.brightness = brightness

        factor = 1

        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1

        im = Image.open(self.tmp_image_path)

        enhancer = ImageEnhance.Brightness(im)

        im_output = enhancer.enhance(factor)
        im_output.save(self.tmp_image_path)

        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint

    def changeContrast(self):
        contrast      = self.parent.contrast_slider.value()
        diff          = contrast - self.contrast
        self.contrast = contrast

        factor = 1
        
        if diff > 0:
            factor = pow(1.2, diff)
        elif diff < 0:
            factor = 1 + diff * 0.1

        im = Image.open(self.tmp_image_path)
        im_output = ImageEnhance.Contrast(im).enhance(factor)
        im_output.save(self.tmp_image_path)
        
        self.image = QImage(self.tmp_image_path)
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint