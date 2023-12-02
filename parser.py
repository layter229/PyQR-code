import shutil
import sys
import qrcode
from PyQt5.QtCore import QDate,QDateTime,QTime
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QVBoxLayout, QWidget, QComboBox, QRadioButton,
                             QButtonGroup, QPushButton, QFileDialog, QCheckBox, QDateTimeEdit)


class QRTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR-Tool")
        self.setWindowIcon(QIcon('qrcode.png'))
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()

        self.setMinimumSize(330, 410)  # Минимальные размеры ширины и высоты окна
        self.setMaximumSize(500, 580)  # Максимальные размеры ширины и высоты окна

        self.text_label = QLabel("Выберете какой QR-код вы хотите создать:")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.text_label)

        # Создайте пространство даты и времени и назначьте текущую дату и время. И изменить формат отображения
        self.dateEdit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.dateEdit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')

        # Установите максимальные и минимальные даты на основе текущей даты, следующего года и предыдущего года
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-2))

        # Установите управление календарем, чтобы разрешить всплывающее окно
        self.dateEdit.setCalendarPopup(True)

        # Триггер функции слота при изменении даты
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        # Триггер функции слота при изменении даты и времени
        self.dateEdit.dateTimeChanged.connect(self.onDateTimeChanged)
        # Trigger при изменении времени
        self.dateEdit.timeChanged.connect(self.onTimeChanged)

        # Создайте пространство даты и времени и назначьте текущую дату и время. И изменить формат отображения
        self.date2Edit = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.date2Edit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')

        # Установите максимальные и минимальные даты на основе текущей даты, следующего года и предыдущего года
        self.date2Edit.setMinimumDate(QDate.currentDate().addDays(-2))

        # Установите управление календарем, чтобы разрешить всплывающее окно
        self.date2Edit.setCalendarPopup(True)

        # Триггер функции слота при изменении даты
        self.date2Edit.dateChanged.connect(self.onDateChanged)
        # Триггер функции слота при изменении даты и времени
        self.date2Edit.dateTimeChanged.connect(self.onDateTimeChanged)
        # Trigger при изменении времени
        self.date2Edit.timeChanged.connect(self.onTimeChanged)

        # Создать кнопку и привязать пользовательский слот
        self.btn = QPushButton('Получить дату и время')
        self.btn.clicked.connect(self.onButtonClick)




        options = ["Текст / Ссылка", "Почта",
                   "Геопозиция", "Телефон", "СМС",
                   "Whatsapp", "Skype", "Zoom",
                   "WiFi", "Визитка", "Календарь"]  # Список элементов ComboBox



        style = ("border: 1px solid #666666;"  # Стиль для QLineEdit
                 "border-radius: 4px")

        self.combo_box = QComboBox()

        self.combo_box.addItems(options)

        # Установка иконок на элементы
        self.combo_box.setItemIcon(0, QIcon('text.png'))
        self.combo_box.setItemIcon(1, QIcon('email.png'))
        self.combo_box.setItemIcon(2, QIcon('geo.png'))
        self.combo_box.setItemIcon(3, QIcon('tel.png'))
        self.combo_box.setItemIcon(4, QIcon('sms.png'))
        self.combo_box.setItemIcon(5, QIcon('whatsapp.png'))
        self.combo_box.setItemIcon(6, QIcon('skype.png'))
        self.combo_box.setItemIcon(7, QIcon('zoom.png'))
        self.combo_box.setItemIcon(8, QIcon('wifi.png'))
        self.combo_box.setItemIcon(9, QIcon('vcard.png'))
        self.combo_box.setItemIcon(10, QIcon('calendar.png'))

        # Установка стилей для ComboBox
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: #ffffff; /* Цвет фона */
                color: #333333; /* Цвет текста */
                border: 1px solid #666666; /* Граница */
                border-radius: 4px; /* Скругленные углы */ 

            }
            QComboBox::item {
                padding: 5px; /* Отступы для текста */
                text-align: center; /* Выравнивание текста по центру */
            }

            QComboBox QAbstractItemView {
                background-color: #f0f0f0; /* Цвет фона выпадающего списка */
                color: #333333; /* Цвет текста в выпадающем списке */
                selection-background-color: #666666; /* Цвет выделенного элемента */
                min-height: 100px; /* Минимальная высота*/
                border: 1px solid #666666; /* Граница */
                border-radius: 4px; /* Скругленные углы */ 
            }
                """)
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_changed)  # Определение индекса элемента
        layout.addWidget(self.combo_box)  # Добавление виджета ComboBox

        self.qr_label = QLabel()  # Добавления виджета с QR-кодом
        pixmap = QPixmap('example_qr.png')
        self.qr_label.setPixmap(pixmap)
        self.imagePath = 'qr.png'
        layout.addWidget(self.qr_label)

        self.save_button = QPushButton("Сохранить QR-код", self)  # Добавление кнопки для сохранения QR-кода
        self.save_button.setGeometry(50, 100, 100, 30)
        self.save_button.setStyleSheet("""
                                        background-color: #ffffff; /* Цвет фона выпадающего списка */

                                        selection-background-color: #666666; /* Цвет выделенного элемента */
                                        border: 1px solid #666666; /* Граница */
                                        border-radius: 4px; /* Скругленные углы */ 
                                       """)
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.text_label2 = QLabel("Введите")
        self.text_label2.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.text_label2)

        self.text_edit = QLineEdit()  # Текст / Ссылка
        self.text_edit.setPlaceholderText("Текст или ссылка")
        self.text_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_edit.setStyleSheet(style)
        self.text_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_edit)
        self.text_edit.setMinimumSize(self.text_edit.sizeHint().width(), 20)

        self.email_edit = QLineEdit()  # Почта
        self.email_edit.setPlaceholderText("e-mail получателя")
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.email_edit.setStyleSheet(style)
        self.email_edit.textChanged.connect(lambda: self.on_text_changed(f'mailto:{self.email_edit.text()}'))
        layout.addWidget(self.email_edit)

        self.geo_edit = QLineEdit()  # Геопозиция
        self.geo_edit.setPlaceholderText("Широта")
        self.geo_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.geo_edit.setStyleSheet(style)
        self.geo2_edit = QLineEdit()
        self.geo2_edit.setPlaceholderText("Долгота")
        self.geo2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.geo2_edit.setStyleSheet(style)
        self.geo2_edit.textChanged.connect(lambda: self.on_text_changed(
            f'geo:{self.geo_edit.text()},{self.geo2_edit.text()}?q={self.geo_edit.text()},{self.geo2_edit.text()}'))
        layout.addWidget(self.geo_edit)
        layout.addWidget(self.geo2_edit)

        self.tel_edit = QLineEdit()  # Телефон
        self.tel_edit.setPlaceholderText("Номер телефона абонента")
        self.tel_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tel_edit.setStyleSheet(style)
        self.tel_edit.textChanged.connect(lambda: self.on_text_changed(f'tel:+{self.tel_edit.text()}'))
        layout.addWidget(self.tel_edit)

        self.sms_edit = QLineEdit()  # СМС сообщение
        self.sms_edit.setPlaceholderText("Номер телефона получателя")
        self.sms_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sms_edit.setStyleSheet(style)
        self.sms_edit.textChanged.connect(lambda: self.on_text_changed(f'SMSTO:+{self.sms_edit.text()}'))
        layout.addWidget(self.sms_edit)

        self.wa_edit = QLineEdit()  # WhatsApp
        self.wa_edit.setPlaceholderText("Номер телефона абонента")
        self.wa_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wa_edit.setStyleSheet(style)
        self.wa2_edit = QLineEdit()
        self.wa2_edit.setPlaceholderText("Сообщение")
        self.wa2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wa2_edit.setStyleSheet(style)
        self.wa_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://wa.me/{self.wa_edit.text()}/?text={self.wa2_edit.text()}'))
        self.wa2_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://wa.me/{self.wa_edit.text()}/?text={self.wa2_edit.text()}'))
        layout.addWidget(self.wa_edit)
        layout.addWidget(self.wa2_edit)

        self.skype_edit = QLineEdit()  # Skype
        self.skype_edit.setPlaceholderText("Имя пользователя")
        self.skype_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.skype_edit.setStyleSheet(style)
        self.chat_but = QRadioButton("chat")
        self.chat_but.setChecked(True)
        self.call_but = QRadioButton("call")
        self.result_but = QLineEdit("chat")
        self.result_but.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.group = QButtonGroup()
        self.group.addButton(self.chat_but)
        self.group.addButton(self.call_but)
        self.group.buttonClicked.connect(self.but_clicked)
        self.group.buttonClicked.connect(
            lambda: self.on_text_changed(f'skype:{self.skype_edit.text()}?{self.result_but.text()}'))
        self.skype_edit.textChanged.connect(
            lambda: self.on_text_changed(f'skype:{self.skype_edit.text()}?{self.result_but.text()}'))
        layout.addWidget(self.skype_edit)
        layout.addWidget(self.chat_but)
        layout.addWidget(self.call_but)
        layout.addWidget(self.result_but)

        self.zoom_edit = QLineEdit()  # Zoom
        self.zoom_edit.setPlaceholderText("ID встречи")
        self.zoom_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom_edit.setStyleSheet(style)
        self.zoom_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://zoom.us/j/{self.zoom_edit.text()}?pwd={self.zoom2_edit.text()}'))
        self.zoom2_edit = QLineEdit()
        self.zoom2_edit.setPlaceholderText("Пароль")
        self.zoom2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom2_edit.setStyleSheet(style)
        self.zoom2_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://zoom.us/j/{self.zoom_edit.text()}?pwd={self.zoom2_edit.text()}'))
        layout.addWidget(self.zoom_edit)
        layout.addWidget(self.zoom2_edit)

        self.wifi_edit = QLineEdit()  # WiFi
        self.wifi_edit.setPlaceholderText("Имя сети")
        self.wifi_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wifi_edit.setStyleSheet(style)
        self.wifi2_edit = QLineEdit()
        self.wifi2_edit.setPlaceholderText("Пароль")
        self.wifi2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wifi2_edit.setStyleSheet(style)
        self.open_but = QRadioButton("")
        self.open_but.setChecked(True)
        self.wpa_but = QRadioButton("T:WPA;")
        self.wep_but = QRadioButton("T:WEP;")
        self.wifi_result_but = QLineEdit("")
        self.wifi_result_but.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.isHidden = QCheckBox()
        self.isHidden.setText("H:true;")
        self.isHidden.stateChanged.connect(self.on_checkbox_state_changed)

        self.wifi_isHidden = QLineEdit("")
        layout.addWidget(self.wifi_isHidden)

        self.wifi_group = QButtonGroup()
        self.wifi_group.addButton(self.open_but)
        self.wifi_group.addButton(self.wpa_but)
        self.wifi_group.addButton(self.wep_but)
        self.wifi_group.buttonClicked.connect(self.wifi_but_clicked)
        self.isHidden.stateChanged.connect(
            lambda: self.on_text_changed(
                f'WIFI:S:{self.wifi_edit.text()};{self.wifi_result_but.text()}P:{self.wifi2_edit.text()};{self.wifi_isHidden.text()};'))
        self.wifi_group.buttonClicked.connect(
            lambda: self.on_text_changed(
                f'WIFI:S:{self.wifi_edit.text()};{self.wifi_result_but.text()}P:{self.wifi2_edit.text()};{self.wifi_isHidden.text()};'))
        self.wifi_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'WIFI:S:{self.wifi_edit.text()};{self.wifi_result_but.text()}P:{self.wifi2_edit.text()};{self.wifi_isHidden.text()};'))
        self.wifi2_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'WIFI:S:{self.wifi_edit.text()};{self.wifi_result_but.text()}P:{self.wifi2_edit.text()};{self.wifi_isHidden.text()};'))
        layout.addWidget(self.wifi_edit)
        layout.addWidget(self.wifi2_edit)
        layout.addWidget(self.isHidden)
        layout.addWidget(self.open_but)
        layout.addWidget(self.wpa_but)
        layout.addWidget(self.wep_but)
        layout.addWidget(self.wifi_result_but)

        self.vcard_edit = QLineEdit()  # Визитка
        self.vcard_edit.setPlaceholderText("Фамилия")
        self.vcard_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard_edit.setStyleSheet(style)

        self.vcard2_edit = QLineEdit()
        self.vcard2_edit.setPlaceholderText("Имя")
        self.vcard2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard2_edit.setStyleSheet(style)

        self.vcard3_edit = QLineEdit()
        self.vcard3_edit.setPlaceholderText("Номер телефона")
        self.vcard3_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard3_edit.setStyleSheet(style)

        self.vcard4_edit = QLineEdit()
        self.vcard4_edit.setPlaceholderText("Дата рождения в формате yyyymmdd")
        self.vcard4_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard4_edit.setStyleSheet(style)

        self.vcard5_edit = QLineEdit()
        self.vcard5_edit.setPlaceholderText("Почта")
        self.vcard5_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard5_edit.setStyleSheet(style)

        self.vcard6_edit = QLineEdit()
        self.vcard6_edit.setPlaceholderText("URL")
        self.vcard6_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard6_edit.setStyleSheet(style)

        self.vcard_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        self.vcard2_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        self.vcard3_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        self.vcard4_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        self.vcard5_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        self.vcard6_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'MECARD: N:{self.vcard_edit.text()}, {self.vcard2_edit.text()};TEL:+{self.vcard3_edit.text()};BDAY:{self.vcard4_edit.text()};EMAIL:{self.vcard5_edit.text()};URL:{self.vcard6_edit.text()};;'))
        layout.addWidget(self.vcard_edit)
        layout.addWidget(self.vcard2_edit)
        layout.addWidget(self.vcard3_edit)
        layout.addWidget(self.vcard4_edit)
        layout.addWidget(self.vcard5_edit)
        layout.addWidget(self.vcard6_edit)

        self.vcal_edit = QLineEdit()  # Визитка
        self.vcal_edit.setPlaceholderText("Дата начала события")
        self.vcal_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcal_edit.setStyleSheet(style)

        self.vcal2_edit = QLineEdit()
        self.vcal2_edit.setPlaceholderText("Дата окончания события")
        self.vcal2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcal2_edit.setStyleSheet(style)

        self.vcal3_edit = QLineEdit()
        self.vcal3_edit.setPlaceholderText("Название события")
        self.vcal3_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcal3_edit.setStyleSheet(style)

        self.vcal4_edit = QLineEdit()
        self.vcal4_edit.setPlaceholderText("URL")
        self.vcal4_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcal4_edit.setStyleSheet(style)


        self.vcal_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:{self.vcal_edit.text()}\nDTEND:{self.vcal2_edit.text()}\nSUMMARY:{self.vcal3_edit.text()}\nURL:http://{self.vcal4_edit.text()}\nCLASS:PUBLIC\nBEGIN:VALARM\nTRIGGER:-PT24H\nACTION:DISPLAY\nDESCRIPTION:Reminder\nEND:VEVENT\nEND:VCALENDAR'))
        self.vcal2_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:{self.vcal_edit.text()}\nDTEND:{self.vcal2_edit.text()}\nSUMMARY:{self.vcal3_edit.text()}\nURL:http://{self.vcal4_edit.text()}\nCLASS:PUBLIC\nBEGIN:VALARM\nTRIGGER:-PT24H\nACTION:DISPLAY\nDESCRIPTION:Reminder\nEND:VEVENT\nEND:VCALENDAR'))
        self.vcal3_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:{self.vcal_edit.text()}\nDTEND:{self.vcal2_edit.text()}\nSUMMARY:{self.vcal3_edit.text()}\nURL:http://{self.vcal4_edit.text()}\nCLASS:PUBLIC\nBEGIN:VALARM\nTRIGGER:-PT24H\nACTION:DISPLAY\nDESCRIPTION:Reminder\nEND:VEVENT\nEND:VCALENDAR'))
        self.vcal4_edit.textChanged.connect(
            lambda: self.on_text_changed(
                f'BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART:{self.vcal_edit.text()}\nDTEND:{self.vcal2_edit.text()}\nSUMMARY:{self.vcal3_edit.text()}\nURL:http://{self.vcal4_edit.text()}\nCLASS:PUBLIC\nBEGIN:VALARM\nTRIGGER:-PT24H\nACTION:DISPLAY\nDESCRIPTION:Reminder\nEND:VEVENT\nEND:VCALENDAR'))
        layout.addWidget(self.vcal_edit)
        layout.addWidget(self.vcal2_edit)
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.date2Edit)
        layout.addWidget(self.btn)
        layout.addWidget(self.vcal3_edit)
        layout.addWidget(self.vcal4_edit)



        # Прячем все виджеты
        self.email_edit.hide()
        self.geo_edit.hide()
        self.geo2_edit.hide()
        self.tel_edit.hide()
        self.sms_edit.hide()
        self.wa_edit.hide()
        self.wa2_edit.hide()
        self.skype_edit.hide()
        self.chat_but.hide()
        self.call_but.hide()
        self.result_but.hide()
        self.zoom_edit.hide()
        self.zoom2_edit.hide()
        self.wifi_edit.hide()
        self.wifi2_edit.hide()
        self.open_but.hide()
        self.wpa_but.hide()
        self.wep_but.hide()
        self.wifi_result_but.hide()
        self.isHidden.hide()
        self.wifi_isHidden.hide()
        self.vcard_edit.hide()
        self.vcard_edit.hide()
        self.vcard2_edit.hide()
        self.vcard3_edit.hide()
        self.vcard4_edit.hide()
        self.vcard5_edit.hide()
        self.vcard6_edit.hide()
        self.vcal_edit.hide()
        self.vcal2_edit.hide()
        self.vcal3_edit.hide()
        self.vcal4_edit.hide()
        self.dateEdit.hide()
        self.date2Edit.hide()
        self.btn.hide()

        # Добавляем рабочее место для виджетов
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        window_size = self.size()
        width = window_size.width()
        height = window_size.height()

        print(f"Ширина: {width}, Высота: {height}")

        # Выполняется при изменении даты

    def onDateChanged(self, date):
        # Выход изменил дату
        print(date)
        # Выполнить независимо от изменения даты или времени

    def onDateTimeChanged(self, dateTime):
        # Выход изменил дату и время
        print(dateTime)
        # Выполнение изменения времени

    def onTimeChanged(self, time):
        # Выход изменил время
        print(time)

    def onButtonClick(self):
        dateTime = self.dateEdit.dateTime()
        # Максимальная дата
        maxDate = self.dateEdit.maximumDate()
        # Максимальное время даты
        maxDateTime = self.dateEdit.maximumDateTime()
        # Максимальное время
        maxTime = self.dateEdit.maximumTime()

        # Минимальная дата
        minDate = self.dateEdit.minimumDate()
        # Минимальная дата и время
        minDateTime = self.dateEdit.minimumDateTime()
        # Минимальное время
        minTime = self.dateEdit.minimumTime()

        print('\ nВыберите время и дату')
        print("Дата и время =% s" % str(dateTime))
        print("Максимальное время даты =% s" % str(maxDateTime))
        print("Макс. Время =% s" % str(maxTime))
        print("Минимальное время даты =% s" % str(minDateTime))
        print("Минимальное время =% s" % str(minTime))
    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            self.wifi_isHidden.setText("H:true;")
        else:
            self.wifi_isHidden.setText("")

    def save_file(self):  # Сохранение QR-кода
        if self.imagePath:
            filename, _ = QFileDialog.getSaveFileName(self, "Куда сохраняем QR-код?", "myqr.png", "PNG (*.png)")
            if filename:
                print("QR-код сохранён, путь до файла: ", filename)
                shutil.copy(self.imagePath, filename)

    def but_clicked(self, button):  # Функция проверки кнопок для Skype
        self.result_but.setText(button.text())

    def wifi_but_clicked(self, button):  # Функция проверки кнопок для WiFi
        self.wifi_result_but.setText(button.text())

    def on_combo_box_changed(self, index):  # Показывать только те виджеты,
        self.text_edit.hide()  # которые нужны для выбранного пункта в ComboBox
        self.email_edit.hide()
        self.geo_edit.hide()
        self.geo2_edit.hide()
        self.tel_edit.hide()
        self.sms_edit.hide()
        self.wa_edit.hide()
        self.wa2_edit.hide()
        self.skype_edit.hide()
        self.chat_but.hide()
        self.call_but.hide()
        self.result_but.hide()
        self.zoom_edit.hide()
        self.zoom2_edit.hide()
        self.wifi_edit.hide()
        self.wifi2_edit.hide()
        self.open_but.hide()
        self.wpa_but.hide()
        self.wep_but.hide()
        self.wifi_result_but.hide()
        self.isHidden.hide()
        self.wifi_isHidden.hide()
        self.vcard_edit.hide()
        self.vcard_edit.hide()
        self.vcard2_edit.hide()
        self.vcard3_edit.hide()
        self.vcard4_edit.hide()
        self.vcard5_edit.hide()
        self.vcard6_edit.hide()
        self.vcal_edit.hide()
        self.vcal2_edit.hide()
        self.vcal3_edit.hide()
        self.vcal4_edit.hide()
        self.dateEdit.hide()
        self.date2Edit.hide()
        self.btn.hide()

        match index:  # switch
            case 0:
                self.text_edit.show()
            case 1:
                self.email_edit.show()
            case 2:
                self.geo_edit.show()
                self.geo2_edit.show()
            case 3:
                self.tel_edit.show()
            case 4:
                self.sms_edit.show()
            case 5:
                self.wa_edit.show()
                self.wa2_edit.show()
            case 6:
                self.skype_edit.show()
                self.chat_but.show()
                self.call_but.show()
            case 7:
                self.zoom_edit.show()
                self.zoom2_edit.show()
            case 8:
                self.wifi_edit.show()
                self.wifi2_edit.show()
                self.open_but.show()
                self.wpa_but.show()
                self.wep_but.show()
                self.isHidden.show()
            case 9:
                self.vcard_edit.show()
                self.vcard_edit.show()
                self.vcard2_edit.show()
                self.vcard3_edit.show()
                self.vcard4_edit.show()
                self.vcard5_edit.show()
                self.vcard6_edit.show()
            case 10:
                self.vcal_edit.show()
                self.vcal2_edit.show()
                self.vcal3_edit.show()
                self.vcal4_edit.show()
                self.dateEdit.show()
                self.date2Edit.show()
                self.btn.show()

        self.adjustSize()  # Корректировка размера окна



    def on_text_changed(self, text):
        # Генерация QR-кода
        qr = qrcode.QRCode()
        print(text)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')  # Сохранение в файл


        if ((text == "MECARD: N:, ;TEL:+;BDAY:;EMAIL:;URL:;;") or
                (text == "mailto:") or (text == "SMSTO:") or
                (text == "tel:") or (text == "geo:") or
                (text == "https://wa.me//?text=") or
                (text == "skype:") or
                (text == "https://zoom.us/j/?pwd=") or
                (text == "WIFI:S:;P:;;")):
            text = ""


        if len(text) > 0:  # Проверка на наличие текста в поле ввода(если его нет, тогда QR-код удаляется)
            pixmap = QPixmap('qr.png')
            self.qr_label.setPixmap(pixmap)
            text = ""
            self.qr_label.setScaledContents(True)
            self.setMaximumSize(440, 620)
            self.adjustSize()
        else:
            self.setMaximumSize(330, 410)
            # self.maximumHeight(400)
            # self.maximumWidth(320)
            pixmap = QPixmap('example_qr.png')
            self.qr_label.setPixmap(pixmap)
            self.qr_label.setScaledContents(True)
            self.setMaximumSize(440, 620)
            self.adjustSize()
            # self.qr_label.clear()


if __name__ == "__main__":  # Main функция для запуска программы
    app = QApplication(sys.argv)
    window = QRTool()
    window.show()
    sys.exit(app.exec_())
