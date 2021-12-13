from PyQt5.QtWidgets import QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

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

            # Сбрасываем значения
            self.parent.zoom_factor = 1

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
        self.image = self.original_image
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

            for row_pixel in range(self.image.width()):
                for col_pixel in range(self.image.height()):
                    pixel = QColor(self.image.pixel(row_pixel, col_pixel))

                    red   = pixel.red()
                    green = pixel.green()
                    blue  = pixel.blue()

        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()