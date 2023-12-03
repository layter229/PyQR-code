import sys
from PyQt5.QtCore import QDate,QDateTime,QTime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DateTimeEditDemo(QWidget):
    def __init__(self):
        super(DateTimeEditDemo, self).__init__()
        self.initUI()
    def initUI(self):
        # Установить заголовок и начальный размер
        self.setWindowTitle('QDateTimeEdit пример')
        self.resize(300,90)

        
        layout=QVBoxLayout()

        # Создайте пространство даты и времени и назначьте текущую дату и время. И изменить формат отображения
        self.dateEdit=QDateTimeEdit(QDateTime.currentDateTime(),self)
        self.dateEdit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')

        # Установите максимальные и минимальные даты на основе текущей даты, следующего года и предыдущего года
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.dateEdit.setMaximumDate(QDate.currentDate().addDays(365))

        # Установите управление календарем, чтобы разрешить всплывающее окно
        self.dateEdit.setCalendarPopup(True)

        # Триггер функции слота при изменении даты
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        # Триггер функции слота при изменении даты и времени
        self.dateEdit.dateTimeChanged.connect(self.onDateTimeChanged)
         #Trigger при изменении времени
        self.dateEdit.timeChanged.connect(self.onTimeChanged)

        # Создать кнопку и привязать пользовательский слот
        self.btn=QPushButton('Получить дату и время')
        self.btn.clicked.connect(self.onButtonClick)

        # Макет управления загрузкой и настройкой
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    # Выполняется при изменении даты
    def onDateChanged(self,date):
        # Выход изменил дату
        print(date)
    # Выполнить независимо от изменения даты или времени
    def onDateTimeChanged(self,dateTime):
        # Выход изменил дату и время
        print(dateTime)
    # Выполнение изменения времени
    def onTimeChanged(self,time):
        # Выход изменил время
        print(time)
    def onButtonClick(self):
        dateTime=self.dateEdit.dateTime()
        # Максимальная дата
        maxDate=self.dateEdit.maximumDate()
        #Максимальное время даты
        maxDateTime=self.dateEdit.maximumDateTime()
        #Максимальное время
        maxTime=self.dateEdit.maximumTime()

        # Минимальная дата
        minDate = self.dateEdit.minimumDate()
        # Минимальная дата и время
        minDateTime=self.dateEdit.minimumDateTime()
        # Минимальное время
        minTime=self.dateEdit.minimumTime()

        print('\ nВыберите время и дату')
        print("Дата и время =% s" %str(dateTime))
        print("Максимальное время даты =% s"%str(maxDateTime))
        print("Макс. Время =% s"%str(maxTime))
        print("Минимальное время даты =% s"%str(minDateTime))
        print("Минимальное время =% s"%str(minTime))

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=DateTimeEditDemo()
    demo.show()
    sys.exit(app.exec_())
