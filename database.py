import sqlite3
import os

class Database:
	""""Класс для работы с базой данных"""

	def connect(self):
		"""Функция осуществляет подлкючение к БД"""

        try:
        	dir_path = os.path.dirname(__file__)
        	DB_PATH  = os.path.join(dir_path, 'database.sqlite')
            self.connect = sqlite3.connect(DB_PATH)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)
