import sqlite3, os

class Database:
    """"Класс для работы с подключением базы данных"""

    def _connect(self):
        """Функция осуществляет подлкючение к БД"""
        
        dir_path = os.path.dirname(__file__)
        DB_PATH = os.path.join(dir_path, 'database.sqlite')

        try:
            self.connect = sqlite3.connect(DB_PATH)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)

    def _close(self):
        """Функция осуществляет отключение от БД"""

        try:
            self.connect.close()
        except Exception as e:
            print(e)

class DatabaseQuery(Database):
    """Класс для работы с запросами в базу данных"""
    
    def getUserPassword(self, username):
        """Функция для получения пароля пользователя"""

        self._connect()
        request = "SELECT password FROM users WHERE username = ?"
        result  = self.cursor.execute(request, (username, )).fetchone()
        self._close()

        if result is None:
            return False
        else:
            return result[0]
        
    def registrateUser(self, username, password_hash):
        """Функция, регистрирующая пользователей в базе данных"""
        
        self._connect()
        request = "INSERT INTO users(username, password) VALUES (?, ?)"
        self.cursor.execute(request, (username, password_hash))
        self.connect.commit()
        self._close()
        
    def getUserImages(self, username):
        """Функция возвращает массив изображений пользователя"""
        
        self._connect()
        request = "SELECT name FROM images WHERE user_id = (SELECT id FROM users WHERE username = ?)"
        result  = self.cursor.execute(request, (username, )).fetchall()
        self._close()
        
        return [i[0] for i in result]