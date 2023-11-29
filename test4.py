import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore


class QRTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR-Tool")

        layout = QVBoxLayout()

        self.text_label = QLabel("Введите текст для создания QR-кода:")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.text_label)

        options = ["Текст / Ссылка", "Почта",
                   "Геопозиция", "Телефон", "СМС",
                   "Whatsapp", "Skype", "Zoom",
                   "WiFi", "Визитка", "Календарь"]
        self.combo_box = QComboBox()
        self.combo_box.addItems(options)
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_changed)
        layout.addWidget(self.combo_box)

        self.qr_label = QLabel()
        layout.addWidget(self.qr_label)

        self.text_edit = QLineEdit()
        # self.text_edit.setStyleSheet("border-style: outset;"
        #                              "border-width: 2px;"
        #                              "border-radius: 5px;"
        #                              "border-color: beige;"
        #                              "font: bold 14px;"
        #                              "min-width: 10em;"
        #                              "padding: 6px;"
        #                              )
        self.text_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.text_edit.textChanged.connect(lambda: self.on_text_changed('', self.text_edit.text()))
        layout.addWidget(self.text_edit)

        self.email_edit = QLineEdit()
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.email_edit.setText("mailto:")
        arg = str("mailto:")
        self.email_edit.textChanged.connect(lambda: self.on_text_changed('mailto:', self.email_edit.text()))
        layout.addWidget(self.email_edit)

        self.geo_edit = QLineEdit()
        self.geo_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        arg = "geo:"
        self.geo_edit.textChanged.connect(lambda: self.on_text_changed('geo:', self.geo_edit.text()))
        layout.addWidget(self.geo_edit)

        self.tel_edit = QLineEdit()
        self.tel_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tel_edit.textChanged.connect(lambda: self.on_text_changed('tel:+', self.tel_edit.text()))
        layout.addWidget(self.tel_edit)

        self.sms_edit = QLineEdit()
        self.sms_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sms_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.sms_edit)

        self.wa_edit = QLineEdit()
        self.wa_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.wa_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.wa_edit)

        self.skype_edit = QLineEdit()
        self.skype_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.skype_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.skype_edit)

        self.zoom_edit = QLineEdit()
        self.zoom_edit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.zoom_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.zoom_edit)

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
        self.tel_edit.hide()
        self.sms_edit.hide()
        self.wa_edit.hide()
        self.skype_edit.hide()
        self.zoom_edit.hide()
        self.wifi_edit.hide()
        self.vcard_edit.hide()
        self.vcal_edit.hide()

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_combo_box_changed(self, index):
        self.text_edit.hide()
        self.email_edit.hide()
        self.geo_edit.hide()
        self.tel_edit.hide()
        self.sms_edit.hide()
        self.wa_edit.hide()
        self.skype_edit.hide()
        self.zoom_edit.hide()
        self.wifi_edit.hide()
        self.vcard_edit.hide()
        self.vcal_edit.hide()

        match index:
            case 0:
                self.text_edit.show()
                arg = ""
            case 1:
                self.email_edit.show()
                arg = "mailto:"
            case 2:
                self.geo_edit.show()
                arg = "geo:"
            case 3:
                self.tel_edit.show()
                arg = "tel:"
            case 4:
                self.sms_edit.show()
                arg = "SMSTO:"
            case 5:
                self.wa_edit.show()
                arg = "https://wa.me/"
            case 6:
                self.skype_edit.show()
                arg = "skype:"
            case 7:
                self.zoom_edit.show()
                arg = "https://zoom.us/j/{id_meet}?pwd={pass}"
            case 8:
                self.wifi_edit.show()
                arg = ""
            case 9:
                self.vcard_edit.show()
                arg = ""
            case 10:
                self.vcal_edit.show()
                arg = ""

        self.adjustSize()

    def on_text_changed(self, args, text):
        qr = qrcode.QRCode()
        url_for_qr = str(args) + text
        print(url_for_qr)

        qr.add_data(url_for_qr)

        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')

        if len(text) > 0:
            pixmap = QPixmap('qr.png')
            self.qr_label.setPixmap(pixmap)
            self.qr_label.setScaledContents(True)
        else:
            self.qr_label.clear()

        self.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRTool()
    window.show()
    sys.exit(app.exec_())