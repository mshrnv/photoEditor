# Стили для слайдеров яркости и контраста
slider = """
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 8px;
            }
            QSlider::sub-page:qlineargradient {
                background: #3B99FC;
                border-radius: 5px;
            }
        """

# Стили для лейблов "Яркость" и "Контраст"
edit_label = """QLabel{font-size: 20px}"""

# Стили для кнопок "Негатив", "Чёрно-белый", "Сепия"
filter_button = """
					QToolButton {
						width: 100%;
						font-size: 15px;
					    border: 1px solid #8f8f91;
					    border-radius: 6px;
					    background-color: white;
					}
				"""

# Стили для всей панели редатирования (применяются после ее отделения от окна)
dock_widget = """
    QDockWidget
    {
        background-color : lightgreen;
        titlebar-close-icon: url(icons/close.png);
        titlebar-normal-icon: url(icons/float.png);
    }
    QDockWidget::title
    {
        background : lightblue;
    }
    QDockWidget::close-button, QDockWidget::float-button {
        padding: 0px;
        icon-size: 20px; /* maximum icon size */
        min-height: 20px;
        min-width: 20px;
    }
"""

# Стили для верхнего меню
menu_bar = """
    QMenuBar {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 lightgray, stop:1 darkgray);
        spacing: 3px; /* spacing between menu bar items */
    }

    QMenuBar::item {
        padding: 1px 4px;
        background: transparent;
        border-radius: 4px;
    }

    QMenuBar::item:selected { /* when selected using mouse or keyboard */
        background: #a8a8a8;
    }

    QMenuBar::item:pressed {
        background: #888888;
    }
"""

# Стили для панели инструментов
tool_bar = """
    QToolBar {
        background: white;
        spacing: 3px; /* spacing between items in the tool bar */
    }
"""