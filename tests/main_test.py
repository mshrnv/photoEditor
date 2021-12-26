import os,sys,inspect
import pytest, sqlite3
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import database
from random import randint

class TestClass:
    
    # Генерация случайного логина, пароля и изображения
    login    = randint(1000,9999)
    password = randint(1000,9999)
    image    = str(randint(1000,9999)) + '.jpg'
    
    # Проверка инициализации объекта класса    
    def test_init(self):
        database.DatabaseQuery()
    
    # Проверка подключения к базе    
    def test_connect(self):
        database.DatabaseQuery()._connect()
    
    # Проверка отключения от базы    
    def test_close(self):
        obj = database.Database()
        obj._connect()
        obj._close()
    
    # Попытка регистрации    
    def test_reg(self):
        database.DatabaseQuery().registrate_user(self.login, self.password)
    
    # Попытка повторной регистрации (ловим ошибку)    
    def test_repeated_reg(self):
        with pytest.raises(sqlite3.IntegrityError):
            database.DatabaseQuery().registrate_user(self.login, self.password)
    
    # Проверка успешной авторизации    
    def test_auth(self):
        assert str(self.password) == database.DatabaseQuery().get_user_password(self.login)
    
    # Попытка добавления изображения    
    def test_image_add(self):
        database.DatabaseQuery().add_image(self.login, self.image)
    
    # Проверка наличия добавленного изображения в базе    
    def test_image_list(self):
        assert True == (self.image in database.DatabaseQuery().get_user_images(self.login))