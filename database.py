"""
    sqlite3 - работа с БД
    os - для работы с путями к файлам
"""
import sqlite3
import os


class Database:
    """
    Класс для работы с подключением базы данных

    Attributes
    ----------
    connect : sqlite3.connect
        Соединение sqlite3 с БД
    cursor : sqlite3.cursor
        Cursor Sqlite3

    Methods
    -------
    _connect()
        Осуществляет подключение к БД
    _close()
        Осуществляет отключение от БД
    """

    def _connect(self):
        """
        Функция подключается к database.sqlite

        """

        # Формируем путь к БД
        dir_path = os.path.dirname(__file__)
        db_path = os.path.join(dir_path, "database.sqlite")

        # Попытка подключения к БД
        try:
            self.connect = sqlite3.connect(db_path)
            self.cursor = self.connect.cursor()

        # В случае ошибки выводим ее в консоль
        except ConnectionError as error:
            print(error)

    def _close(self):
        """
        Функция отключается от БД database.sqlite

        """

        # Попытка отключения от БД
        try:
            self.connect.close()

        # В случае ошибки выводим ее в консоль
        except ConnectionError as error:
            print(error)


class DatabaseQuery(Database):
    """
    Класс для работы с запросами в базу данных

    Args:
        Database (Class): Для управления подключением к БД
    """

    def get_user_password(self, username):
        """
        Функция возвращает пароль пользователя username

        Args:
            username (String): Логин пользователя

        Returns:
            String|Boolean: Хэш пароля, если такой пользователь есть, False - в обратном случае
        """

        # Подключение к БД
        self._connect()

        # Формируем и исполняем запрос к БД
        request = "SELECT password FROM users WHERE username = ?"
        result = self.cursor.execute(request, (username,)).fetchone()

        # Отключаемся от БД
        self._close()

        # Если ответ None - значит пользователя с таким ником не существует
        if result is None:
            return False

        # Иначе - возвращаем хэш пароля из БД
        return result[0]

    def registrate_user(self, username, password_hash):
        """
        Функция регистрирует пользователей в базе данных

        Args:
            username      (string): Логин пользоватедя
            password_hash (string): Хэш пароля пользователя

        """

        # Подключение к БД и формирование запроса
        self._connect()
        request = "INSERT INTO users(username, password) VALUES (?, ?)"

        # Исполнение запроса и подтверждение изменения базы
        self.cursor.execute(request, (username, password_hash))
        self.connect.commit()

        self._close()

    def get_user_images(self, username):
        """
        Функция возвращает массив изображений пользователя

        Args:
            username (string): Логин пользователя

        Returns:
            List: Список названий изображений
        """

        # Подключение к БД и формирование запроса
        self._connect()
        request = "SELECT name FROM images WHERE user_id = (SELECT id FROM users WHERE username=?)"

        # Получение данных из базы и отключение от БД
        result = self.cursor.execute(request, (username,)).fetchall()
        self._close()

        # Возврат результата в виде списка строк
        return [i[0] for i in result]

    def add_image(self, username, basename):
        """
        Функция для добавления загруженного изображения в БД

        Args:
            username (string): Логин пользователя
            basename (string): Имя файла с изображением
        """

        # Подклчение к БД, формирование и исполнение запроса
        self._connect()
        request = "INSERT INTO images(name, user_id) VALUES (?, (SELECT id FROM users WHERE username = ?))"
        self.cursor.execute(request, (basename, username))

        # Подтверждение изменений и отключение от БД
        self.connect.commit()
        self._close()
