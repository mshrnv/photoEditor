import sqlite3
import os

class Database:
	""""����� ��� ������ � ����� ������"""

	def connect(self):
		"""������� ������������ ����������� � ��"""

        try:
        	dir_path = os.path.dirname(__file__)
        	DB_PATH  = os.path.join(dir_path, 'database.sqlite')
            self.connect = sqlite3.connect(DB_PATH)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)

    def close(self):
    	"""������� ������������ ���������� �� ��"""
    	
    	try:
            self.connect.close()
        except Exception as e:
            print(e)

    def getUserPassword(self, username):
        """������� ��� ��������� ������ ������������"""

        self.connect()
        request = "SELECT password FROM users WHERE username = ?"
        result  = self.cursor.execute(request, (date,time)).fetchone()