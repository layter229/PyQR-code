import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QComboBox, QRadioButton, \
    QButtonGroup
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore


class QRTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR-Tool")
        self.setWindowIcon(QIcon('qrcode.png'))
        self.setStyleSheet("background-color: white;")



        layout = QVBoxLayout()



        self.text_label = QLabel("Выберете какой QR-код вы хотите создать:")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.text_label)


        options = ["Текст / Ссылка", "Почта",
                   "Геопозиция", "Телефон", "СМС",
                   "Whatsapp", "Skype", "Zoom",
                   "WiFi", "Визитка", "Календарь"]


        self.combo_box = QComboBox()

        self.combo_box.addItems(options)
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
            }
            
                """)
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_changed)
        layout.addWidget(self.combo_box)


        self.qr_label = QLabel()
        layout.addWidget(self.qr_label)


        self.text_edit = QLineEdit()
        self.text_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_edit.setStyleSheet("border: 1px solid #666666;"
                                     "border-radius: 4px")

        self.text_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_edit)
        self.text_edit.setMinimumSize(self.text_edit.sizeHint().width(), 20)


        self.email_edit = QLineEdit()
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.email_edit.textChanged.connect(lambda: self.on_text_changed(f'mailto:{self.email_edit.text()}'))
        layout.addWidget(self.email_edit)


        self.geo_edit = QLineEdit()
        self.geo_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.geo2_edit = QLineEdit()
        self.geo2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.geo2_edit.textChanged.connect(lambda: self.on_text_changed(
            f'geo:{self.geo_edit.text()},{self.geo2_edit.text()}?q={self.geo_edit.text()},{self.geo2_edit.text()}'))
        layout.addWidget(self.geo_edit)
        layout.addWidget(self.geo2_edit)


        self.tel_edit = QLineEdit()
        self.tel_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tel_edit.textChanged.connect(lambda: self.on_text_changed(f'tel:+{self.tel_edit.text()}'))
        layout.addWidget(self.tel_edit)


        self.sms_edit = QLineEdit()
        self.sms_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sms_edit.textChanged.connect(lambda: self.on_text_changed(f'SMSTO:{self.sms_edit.text()}'))
        layout.addWidget(self.sms_edit)


        self.wa_edit = QLineEdit()
        self.wa_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wa2_edit = QLineEdit()
        self.wa2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wa2_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://wa.me/{self.wa_edit.text()}/?text={self.wa2_edit.text()}'))
        layout.addWidget(self.wa_edit)
        layout.addWidget(self.wa2_edit)


        self.skype_edit = QLineEdit()
        self.skype_edit.setAlignment(Qt.AlignmentFlag.AlignTop)

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


        self.zoom_edit = QLineEdit()
        self.zoom_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom2_edit = QLineEdit()
        self.zoom2_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom2_edit.textChanged.connect(
            lambda: self.on_text_changed(f'https://zoom.us/j/{self.zoom_edit.text()}?pwd={self.zoom2_edit.text()}'))
        layout.addWidget(self.zoom_edit)
        layout.addWidget(self.zoom2_edit)


        self.wifi_edit = QLineEdit()
        self.wifi_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wifi_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.wifi_edit)


        self.vcard_edit = QLineEdit()
        self.vcard_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcard_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.vcard_edit)


        self.vcal_edit = QLineEdit()
        self.vcal_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vcal_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.vcal_edit)


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
        self.vcard_edit.hide()
        self.vcal_edit.hide()


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def but_clicked(self, button):
        self.result_but.setText(button.text())

    def on_combo_box_changed(self, index):
        self.text_edit.hide()
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
        self.vcard_edit.hide()
        self.vcal_edit.hide()

        match index:
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
            case 9:
                self.vcard_edit.show()
            case 10:
                self.vcal_edit.show()

        self.adjustSize()

    def on_text_changed(self, text):
        qr = qrcode.QRCode()
        # url_for_qr = str(args) + text
        print(text)

        qr.add_data(text)

        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')

        if len(text) > 0:
            pixmap = QPixmap('qr.png')
            self.qr_label.setPixmap(pixmap)
            self.qr_label.setScaledContents(True)
        else:
            self.qr_label.clear()

        # if (len(self.text_edit.text()) or len(self.text_edit.text()) or
        #     len(self.text_edit.text()) or len(self.text_edit.text()) or
        #     len(self.text_edit.text()) or len(self.text_edit.text()) or
        #     len(self.text_edit.text()) or len(self.text_edit.text()) or
        #     len(self.text_edit.text()) or len(self.text_edit.text())) > 0:
        #         self.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRTool()
    window.show()
    sys.exit(app.exec_())
