import sqlite3, os

class Database:
    """"Класс для работы с базой данных"""

    def connect(self):
        """Функция осуществляет подлкючение к БД"""
        
        dir_path = os.path.dirname(__file__)
        DB_PATH = os.path.join(dir_path, 'database.sqlite')

        try:
            self.connect = sqlite3.connect(DB_PATH)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)

    def close(self):
        """Функция осуществляет отключение от БД"""

        try:
            self.connect.close()
        except Exception as e:
            print(e)

    def getUserPassword(self, username):
        """Функция для получения данных пользователя"""

        self.connect()
        request = "SELECT password FROM users WHERE username = ?"
        result  = self.cursor.execute(request, (username, )).fetchone()
        self.close()

        if result is None:
            return False
        else:
            return result[0]                                                                         '))