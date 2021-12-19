# photoEditor

Фоторедактор, реализованный на Python + PyQt5 + Pillow

## Developers Team:
    1. Maintainer - 2020-5-24-sho
    2. Developer  - 2020-5-21-tak
    3. Developer  - 2020-5-01-abr
    4. Developer  - 2020-5-23-shi

## Цели:
    1. Выкатить вторую версию фоторедактора
    2. Спроектировать БД, хранящую информацию о пользователях и изображениях
    3. Добавить окно авторизации, регистрации пользователей
    4. Добавить окно загрузки/выбора изображения для текущего пользователя
    5. Напиать тесты, протестировать
    6. Отформатировать код, привести к единой стилистике
    7. Добавить обработку исключений в коде приложения

## Важная информация:
В связи с переходом на редактирование изображения с помощью библиотеки Pillow, меняю задачи  
Постарайтесь сделать как можно быстрее, объем работ будет увеличен

### Задачи для maintainer:
* [x] Добавить README.md с текущими целями
* [x] Добавить requirements.txt, со списком всех библиотек, используемых в проекте
* [x] Пересобрать главный класс фоторедактора, сделать формирование дизайна функционально
* [x] Реализовать ```createMainLabel()```, рисующую главный label
* [x] Убрать ненужный функционал при открытии главного окна приложения
* [x] Написать стили для текущих компонентов, удобно расположить компоненты на окне
* [x] Связать функции наложения фильтров с нажатием на соответсвующие кнопки
* [x] Реализовать хранение файлов и убрать неактуальные свойства класса Image
* [x] Спроектировать и создать БД, реализовать класс для работы с ней
* [ ] Связать все окна между собой (подробное описание в issue)

### Задачи для developer-2:
* [x] Реализовать запуск окна, согласно дизайну 
* [x] Реализовать ```createEditingBar```, рисующую панель редактирования
* [x] Привести названия переменных и функций к единому стилю 
* [x] Реалзовать открытие файла
* [x] Реалзовать функцию ```saveImage```, сохраняющую изображение
* [x] Реализовать наложение фильтра Сепия
* [x] Реализовать с помощью библиотеки Pillow наложение фильтров
* [x] Покрыть код комментариями для упрощения читабельности
* [x] Спроектировать и создать окно выбора изображения из списка изображений пользователя

### Задачи для developer-3:
* [x] Сфорировать **design.py** согласно **design.ui**
* [x] Реализовать ```createMenu```, рисующую меню
* [x] Покрыть код комментариями  
* [x] Добавить иконки к элементам меню
* [x] Реализовать функцию ```updateActions``` (Описание укажу в issue)
* [x] Переделать все названия QActions на русский язык
* [x] Реализовать наложение фильтра Негатив
* [x] Реализовать отражение и поворот изображения с помощью Pillow
* [x] Добавить новые стили
* [x] Спроектировать и создать окно авторизации/регистрации пользователей

### Задачи для developer-4:
* [x] Задизайнить окно фоторедактора в QT Designer, на выходе **design.ui**
* [x] Реализовать ```createToolBar```, рисующую панель инструментов
* [x] Разбить ```main.py``` на несколько файлов
* [x] Реализовать закрытие приложения нажатием на кнопку
* [x] Реализовать функцию ```revertToOriginal``` (Описание укажу в issue)
* [x] Реализовать наложение фильтра ЧБ
* [x] Пофиксить все иконки, отказаться от зума фотографии на экране и обрезания фото
* [x] Реализовать сброс всех кнопок при отмене изменений или загрузке новой фотографии
* [x] Рефакторинг кода, исправить баги
* [ ] Отформатировать код с помощью black formatter, добавить обработку исключений

### Задачи на перспективу:
* [x] Сформировать *about* и реализовать в виде MessageBox принажатии на кнопку в меню
* [ ] Создать для каждого исключения его обработку и вывод в `QErrorMessage`
