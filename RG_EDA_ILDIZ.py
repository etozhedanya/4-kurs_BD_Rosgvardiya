
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMainWindow, QVBoxLayout, QWidget, QLabel, QAction, Qt, QMessageBox, QApplication, QFileDialog
import pymysql

login = 'MilyaSheih'
psswrd = 'Kazah'
sreg = 0
tablnum = 0

class Window3(QWidget): #класс окна журнала вызова
    
    def pechat(self):
        global tablnum
        with open('Отчёт.txt', 'w', encoding='UTF-8') as out_file:
            if tablnum == 1:
                print("------------------------------------------------", file=out_file)
                print("| ID Экипажа | Название | Дата | Время | Адрес |", file=out_file)
                print("------------------------------------------------", file=out_file)
            else:
                print("-------------------------------------------------", file=out_file)
                print("| ID Вызова | ID Экипажа | Дата | Время | Адрес |", file=out_file)
                print("-------------------------------------------------", file=out_file)
            for row in range(self.tableWidget.rowCount()):
                for column in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, column)
                    print('|'+item.text(), end='| ', file=out_file) 
                print('', file=out_file)  

    def dobavzp(self):#функция добавления
        #переменные для ввода в таблицу бд
        idvz = self.lineEdit.text()
        idek = self.lineEdit_2.text()
        dat = self.lineEdit_3.text()
        tim = self.lineEdit_4.text()
        adres = self.lineEdit_5.text()

        #подключаемся к бд
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            #команда ввода в бд
            sqlquery = f"INSERT INTO call_log VALUES({idvz},{idek},'{dat}','{tim}','{adres}')"
            result = cur.execute(sqlquery)
            con.commit()

            #очищаем таблицу и заново заполняем её(обновляем)
            self.tableWidget.clear()
            self.loadbd()#вызов функции обновления
        #обработчики ошибок
        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Дублирование данных!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    def udalzp(self): #функция удаления
        #переменная айди вызова
        idvz = self.lineEdit_6.text()

        #подключаемся к бд
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            #команда ввода в бд
            sqlquery = f"DELETE FROM call_log WHERE Id_vizova = {idvz}"
            result = cur.execute(sqlquery)
            con.commit()
            
            #очищаем таблицу и заново заполняем её(обновляем)
            self.tableWidget.clear()
            self.loadbd()#вызов функции обновления

        #обработчики ошибок
        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Поле привязанно к другой таблице!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    def zapros(self):#функция запроса
        global tablnum
        zaprs = self.lineEdit_7.text()#переменная введённого условия в запрос
        cmbx = self.comboBox.currentText()#переменная выбранного пункта в комбо бокс 1
        cmbx2 = self.comboBox_2.currentText()#переменная выбранного пункта в комбо бокс 2

        #подключаемся к бд
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()

        #если в комбо боксе 1 выбрано запрос по времени, то...
        try:
            if cmbx == 'Времени':
                cur = con.cursor()
                #если в комбо боксе 2 выбрано ДО, то...
                if cmbx2 == "До":
                    sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Time <'{zaprs}'"
                #если в комбо боксе 2 выбрано ДО, то...
                if cmbx2 == "После":
                    sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Time >'{zaprs}'"
                result = cur.execute(sqlquery)
                con.commit()
                itog = cur.fetchall()
                cc = 5
            #если в комбо боксе 1 выбрано запрос по Дате, то...
            elif cmbx == 'Дате':
                cur = con.cursor()
                if cmbx2 == "До":
                    sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Data <'{zaprs}'"
                if cmbx2 == "После":
                    sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Data >'{zaprs}'"
                result = cur.execute(sqlquery)
                con.commit()
                itog = cur.fetchall()
                cc = 5
            #если в комбо боксе 1 выбрано запрос по Адресу, то...   
            elif cmbx == 'Адресу':
                cur = con.cursor()
                sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Adress_vizova ='{zaprs}'"
                result = cur.execute(sqlquery)
                con.commit()
                itog = cur.fetchall()
                cc = 5
            #если в комбо боксе 1 выбрано запрос по Экипажу, то...
            elif cmbx == 'Экипажу':
                cur = con.cursor()
                sqlquery = f"SELECT Call_Log.Id_ekipaja, Nazvanie_ekipaja.Name, Call_Log.Data, Call_Log.Time, Call_Log.Adress_vizova FROM Nazvanie_ekipaja INNER JOIN Call_Log ON Nazvanie_ekipaja.Id_ekipaja = Call_Log.Id_ekipaja WHERE Call_Log.Id_ekipaja ={zaprs}"
                result = cur.execute(sqlquery)
                con.commit()
                itog = cur.fetchall()
                cc = 5
            
            #очищаем таблицу
            self.tableWidget.clear()

            #заранее приравняем переменные строки и стоблца к 0
            row = 0
            column = 0

            #сзададим таблице значения их строки и колонок, как в таблице бд
            self.tableWidget.setRowCount(len(itog))
            self.tableWidget.setColumnCount(cc)

            for i in itog:
                for k in i:
                    #берём каждый элемент из таблицы бд и вписываем его в таблицу пайтон
                    self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                    if column == cc - 1:
                        row += 1
                        column = 0
                    else:
                        column += 1

            self.tableWidget.resizeColumnToContents(True)
            self.tableWidget.setHorizontalHeaderLabels(["ID Экипажа", "Название", "Дата", "Время", "Адрес"])
            tablnum = 1

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный запрос")
            
    
    def loadbd(self):#функция обновления
        #подключаемся к бд
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        #команда вывода всех жанных
        sqlquery = "SELECT*FROM call_log"
        cur = con.cursor()
        result = cur.execute(sqlquery)
        itog = cur.fetchall()

        row = 0
        column = 0
        self.tableWidget.setRowCount(len(itog))
        #аналогично как сверху
        for i in itog:
            for k in i:
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                if column == 4:
                    row += 1
                    column = 0
                else:
                    column += 1
        self.tableWidget.setHorizontalHeaderLabels(["ID Вызова", "ID Экипажа", "Дата", "Время", "Адрес"])
        tablnum = 0
    
    def __init__(self):#функция интерфейса
        super(Window3, self).__init__()
        self.setWindowTitle('Журнал вызовов')
        self.setMinimumWidth(521)
        self.setMinimumHeight(343)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 501, 192))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(310, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(410, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(9, 230, 503, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(10, 260, 113, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(121, 259, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(378, 260, 131, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(368, 281, 141, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(300, 281, 70, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-1, -5, 521, 351))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("экипаж.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(299, 301, 211, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(9, 301, 190, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setDefault(True)
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(298, 260, 81, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_2.raise_()
        self.tableWidget.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_3.raise_()
        self.lineEdit_4.raise_()
        self.lineEdit_5.raise_()
        self.pushButton.raise_()
        self.lineEdit_6.raise_()
        self.pushButton_2.raise_()
        self.pushButton_4.raise_()
        self.comboBox.raise_()
        self.lineEdit_7.raise_()
        self.comboBox_2.raise_()
        self.pushButton_3.raise_()
        self.lineEdit_11.raise_()
        self.tableWidget.verticalHeader().hide()

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Журнал вызовов"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID Вызова"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID Экипажа"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Дата"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Время"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Адрес"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.lineEdit_6.setText(_translate("MainWindow", "ID вызова"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_4.setText(_translate("MainWindow", "Печать"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Экипажу"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Времени"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Дате"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Адресу"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "До"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "После"))
        self.pushButton_3.setText(_translate("MainWindow", "Провести запрос"))
        self.lineEdit_11.setText(_translate("MainWindow", "Вывести по"))

        self.loadbd()#вызываем обновление таблицы
        #привязываем кнопки к функциям
        self.pushButton.clicked.connect(self.dobavzp)
        self.pushButton_2.clicked.connect(self.udalzp)
        self.pushButton_3.clicked.connect(self.zapros)
        self.pushButton_4.clicked.connect(self.pechat)
        


class Window2(QWidget):#класс окна экипажа, внутри всё аналогично, как сверху
    def loadbd(self):
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        sqlquery = "SELECT*FROM ekipaj"
        cur = con.cursor()
        result = cur.execute(sqlquery)
        itog = cur.fetchall()

        row = 0
        column = 0
        self.tableWidget_2.setRowCount(len(itog))

        for i in itog:
            for k in i:
                self.tableWidget_2.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                if column == 1:
                    row += 1
                    column = 0
                else:
                    column += 1

        sqlquery = "SELECT*FROM nazvanie_ekipaja"
        cur = con.cursor()
        result = cur.execute(sqlquery)
        itog = cur.fetchall()

        row = 0
        column = 0
        self.tableWidget.setRowCount(len(itog))

        for i in itog:
            for k in i:
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                if column == 1:
                    row += 1
                    column = 0
                else:
                    column += 1
        self.tableWidget.setHorizontalHeaderLabels(["ID Экипажа", "Название"])
        self.tableWidget_2.setHorizontalHeaderLabels(["ID Экипажа", "ID Сотрудника"])

    def dobavzp1(self):
        idek = self.lineEdit_4.text()
        naz = self.lineEdit_5.text()

        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"INSERT INTO ekipaj VALUES({idek},'{naz}')"
            result = cur.execute(sqlquery)
            con.commit()

            self.tableWidget.clear()
            self.tableWidget_2.clear()
            self.loadbd()

        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Дублирование данных!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    def udalzp1(self):
        ids = self.lineEdit_8.text()
        idek = self.lineEdit_10.text()
        
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"DELETE FROM ekipaj WHERE Id_sotrudnika = {ids} and Id_ekipaja = {idek}"
            result = cur.execute(sqlquery)
            con.commit()
            
            self.tableWidget.clear()
            self.tableWidget_2.clear()
            self.loadbd()

        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Поле привязано к другой таблице!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    def dobavzp2(self):
        idek = self.lineEdit.text()
        naz = self.lineEdit_2.text()

        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"INSERT INTO nazvanie_ekipaja VALUES({idek},'{naz}')"
            result = cur.execute(sqlquery)
            con.commit()

            self.tableWidget.clear()
            self.tableWidget_2.clear()
            self.loadbd()

        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Дублирование данных!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    def udalzp2(self):
        idek = self.lineEdit_6.text()
        
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"DELETE FROM nazvanie_ekipaja WHERE Id_ekipaja = {idek}"
            result = cur.execute(sqlquery)
            con.commit()
            
            self.tableWidget.clear()
            self.tableWidget_2.clear()
            self.loadbd()

        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Поле привязано к другой таблице!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

    
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Экипажи')
        self.setMinimumWidth(521)
        self.setMinimumHeight(291)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 201, 192))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(9)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(310, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(410, 210, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(9, 230, 203, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(10, 260, 129, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(137, 259, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(310, 10, 201, 192))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(9)
        font.setBold(True)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(309, 230, 203, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(311, 250, 129, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(311, 270, 129, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setObjectName("lineEdit_10")
        
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(438, 259, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-1, -5, 521, 301))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("1.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.raise_()
        self.tableWidget.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_4.raise_()
        self.lineEdit_5.raise_()
        self.pushButton.raise_()
        self.lineEdit_6.raise_()
        self.pushButton_2.raise_()
        self.tableWidget_2.raise_()
        self.pushButton_3.raise_()
        self.lineEdit_8.raise_()
        self.lineEdit_10.raise_()
        self.pushButton_4.raise_()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget_2.verticalHeader().hide()

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Экипажи"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID Экипажа"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Название"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.lineEdit_6.setText(_translate("MainWindow", "ID экипажа"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID Экипажа"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID Сотрудника"))
        self.pushButton_3.setText(_translate("MainWindow", "Добавить"))
        self.lineEdit_8.setText(_translate("MainWindow", "ID сотрудника"))
        self.lineEdit_10.setText(_translate("MainWindow", "ID экипажа"))
        self.pushButton_4.setText(_translate("MainWindow", "Удалить"))

        self.loadbd()
        self.pushButton.clicked.connect(self.dobavzp2)
        self.pushButton_2.clicked.connect(self.udalzp2)
        self.pushButton_3.clicked.connect(self.dobavzp1)
        self.pushButton_4.clicked.connect(self.udalzp1)

class Window1(QWidget):#класс окна сотрудников, внутри всё аналогично, как сверху
    def loadbd(self):
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        sqlquery = "SELECT*FROM sotrudniki"
        cur = con.cursor()
        result = cur.execute(sqlquery)
        itog = cur.fetchall()

        row = 0
        column = 0
        self.tableWidget.setRowCount(len(itog))

        for i in itog:
            for k in i:
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                if column == 4:
                    row += 1
                    column = 0
                else:
                    column += 1

        for i in range(len(itog)):
            try:
                idsotr = self.tableWidget.item(i,0).text()
                sqlquery = "SELECT Id_ekipaja FROM ekipaj WHERE Id_sotrudnika=" + idsotr
                result = cur.execute(sqlquery)
                itog = cur.fetchall()
                idekip = itog[0][0]
                sqlquery = "SELECT Name FROM nazvanie_ekipaja WHERE Id_ekipaja=" + str(idekip)
                result = cur.execute(sqlquery)
                itog = cur.fetchall()
                self.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(itog[0][0])))
                self.tableWidget.verticalHeader().hide()
            except:
                p = 0
        self.tableWidget.setHorizontalHeaderLabels(["ID Сотрудника", "Ф.И.О.", "Телефон", "Адрес", "Звание", "Экипаж"])
            
    def dobavzp(self):
        ids = self.lineEdit_3.text()
        fio = self.lineEdit_7.text()
        tel = self.lineEdit_8.text()
        adres = self.lineEdit_9.text()
        zv = self.lineEdit_10.text()

        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"INSERT INTO sotrudniki VALUES({ids},'{fio}',{tel},'{adres}','{zv}')"
            result = cur.execute(sqlquery)
            con.commit()
            
            self.tableWidget.clear()
            self.loadbd()
        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")

        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Дублирование данных!")

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пустой ввод данных!")

        

    def udalzp(self):
        ids = self.lineEdit_6.text()
        
        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        try:
            sqlquery = f"DELETE FROM sotrudniki WHERE Id_sotrudnika = {ids}"
            result = cur.execute(sqlquery)
            con.commit()
            
            self.tableWidget.clear()
            self.loadbd()

        except pymysql.err.ProgrammingError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Пусто!")
        
        except pymysql.err.OperationalError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Некорректный ввод данных!")
        
        except pymysql.err.IntegrityError:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                "Сотрудник привязан к другой таблице!")

    def zapros(self):
        zaprs = self.lineEdit_11.text()
        cmbx = self.comboBox.currentText()

        con = pymysql.connect(
        host = 'localhost',
        database = 'rosguard1',
        user = 'root',
        passwd = '1111')
        cur = con.cursor()
        
        if cmbx == 'Званию':
            cur = con.cursor()
            sqlquery = f"SELECT * FROM Sotrudniki WHERE Zvanie ='{zaprs}'"
            result = cur.execute(sqlquery)
            con.commit()
            itog = cur.fetchall()
            cc = 5
          
            
            
        elif cmbx == 'По 1-ым буквам':
            cur = con.cursor()
            sqlquery = f"SELECT * FROM Sotrudniki WHERE F_I_O LIKE '{zaprs}%'"
            result = cur.execute(sqlquery)
            con.commit()
            itog = cur.fetchall()
            cc = 5
            

        elif cmbx == 'Экипажу':
            cur = con.cursor()
            sqlquery = f"SELECT Ekipaj.Id_ekipaja, Nazvanie_ekipaja.Name, Sotrudniki.F_I_O, Sotrudniki.Zvanie FROM Sotrudniki INNER JOIN (Nazvanie_ekipaja INNER JOIN Ekipaj ON Nazvanie_ekipaja.Id_ekipaja = Ekipaj.Id_ekipaja) ON Sotrudniki.Id_sotrudnika = Ekipaj.Id_sotrudnika WHERE Nazvanie_ekipaja.Name='{zaprs}'"
            result = cur.execute(sqlquery)
            con.commit()
            itog = cur.fetchall()
            cc = 4
        
        
        self.tableWidget.clear()

        self.tableWidget.setHorizontalHeaderLabels(["ID Сотрудника", "Ф.И.О.", "Телефон", "Адрес", "Звание"])
        if cmbx == 'Экипажу':
            self.tableWidget.setHorizontalHeaderLabels(["ID Отряда", "Название", "ФИО", "Адрес", "Звание"])

        row = 0
        column = 0
        self.tableWidget.setRowCount(len(itog))
        self.tableWidget.setColumnCount(cc)

        for i in itog:
            for k in i:
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(k)))
                if column == cc - 1:
                    row += 1
                    column = 0
                else:
                    column += 1

        self.tableWidget.resizeColumnToContents(True)
        
    
    def __init__(self):
        super(Window1, self).__init__()
        self.setWindowTitle('Сотрудники')
        self.setMinimumWidth(621)
        self.setMinimumHeight(497)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(4, 5, 611, 201))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.tableWidget.setFont(font)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(9)
        font.setBold(True)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(173, 56, 35))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(8, 280, 161, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 440, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(7, 465, 141, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(8, 305, 31, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setText("")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 304, 131, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setDefault(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(440, 280, 131, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-5, -8, 631, 511))
        self.label_2.setToolTipDuration(0)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("сотрудники.jpg"))
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(120, 440, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(230, 440, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(341, 440, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(452, 440, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(350, 280, 81, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 304, 221, 24))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2.raise_()
        self.tableWidget.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_3.raise_()
        self.pushButton.raise_()
        self.lineEdit_6.raise_()
        self.pushButton_2.raise_()
        self.comboBox.raise_()
        self.lineEdit_7.raise_()
        self.lineEdit_8.raise_()
        self.lineEdit_9.raise_()
        self.lineEdit_10.raise_()
        self.lineEdit_11.raise_()
        self.pushButton_3.raise_()


        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Сотрудники"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID Сотрудника"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Ф.И.О."))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Телефон"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Адрес"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Звание"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Экипаж"))
        self.lineEdit_2.setText(_translate("MainWindow", "Введите ID сотрудника"))
        self.lineEdit_3.setText(_translate("MainWindow", "Id"))
        self.pushButton.setText(_translate("MainWindow", "Добавить запись"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить запись"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Званию"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Экипажу"))
        self.comboBox.setItemText(2, _translate("MainWindow", "По 1-ым буквам"))
        self.lineEdit_7.setText(_translate("MainWindow", "Ф.И.О."))
        self.lineEdit_8.setText(_translate("MainWindow", "Телефон"))
        self.lineEdit_9.setText(_translate("MainWindow", "Адрес"))
        self.lineEdit_10.setText(_translate("MainWindow", "Звание"))
        self.lineEdit_11.setText(_translate("MainWindow", "Вывести по"))
        self.pushButton_3.setText(_translate("MainWindow", "Провести запрос"))

        self.loadbd()
        self.pushButton.clicked.connect(self.dobavzp)
        self.pushButton_2.clicked.connect(self.udalzp)
        self.pushButton_3.clicked.connect(self.zapros)

class Ui_MainWindow(object):#класс глвного меню
    
    def registr(self):#функция вызова окна с сотрудниками
        global sreg, login, psswrd
        lg = self.lineEdit_8.text()
        pwd = self.lineEdit_9.text()
        if lg == login and pwd == psswrd:
            sreg = 1
            QtWidgets.QMessageBox.warning(MainWindow, "Логин",
                "Успешный вход!")
        else:
            sreg = 0
            QtWidgets.QMessageBox.warning(MainWindow, "Ошибка",
                "Некорректные данные для входа!")
        
    def sotr(self):#функция вызова окна с сотрудниками
        global sreg, login, psswrd
        if sreg == 1:
            self.w1 = Window1()
            self.w1.show()
        else:
            QtWidgets.QMessageBox.warning(MainWindow, "Ошибка",
                "Для начала работы авторизируйтесь в бд!")
            
    def ekip(self):#функция вызова окна с экипажем
        global sreg, login, psswrd
        if sreg == 1:
            self.w2 = Window2()
            self.w2.show()
        else:
            QtWidgets.QMessageBox.warning(MainWindow, "Ошибка",
                "Для начала работы авторизируйтесь в бд!")
    def zhrnl(self):#функция вызова окна с журналом
        global sreg, login, psswrd
        if sreg == 1:
            self.w3 = Window3()
            self.w3.show()
        else:
            QtWidgets.QMessageBox.warning(MainWindow, "Ошибка",
                "Для начала работы авторизируйтесь в бд!")

    def setupUi(self, MainWindow):#функция интерфейса
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(498, 387)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(3, 2, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setIconSize(QtCore.QSize(150, 100))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 3, 91, 31))

        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(30, 290, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")
        
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(30, 320, 101, 22))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_9.setEchoMode(QtWidgets.QLineEdit.Password)
        
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setDefault(True)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(234, 3, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(387, 3, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setDefault(True)
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 491, 361))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("титул.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.lineEdit_8.raise_()
        self.lineEdit_9.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_13 = QtWidgets.QAction(MainWindow)
        self.action_13.setObjectName("action_13")
        self.menu.addAction(self.action_11)
        self.menu.addAction(self.action_13)
        self.menubar.addAction(self.menu.menuAction())


        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(130, 290, 50, 50))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setIconSize(QtCore.QSize(150, 100))
        self.pushButton_6.setCheckable(False)
        self.pushButton_6.setAutoRepeat(False)
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setDefault(True)
        self.pushButton_6.setFlat(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.raise_()

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.sotr)
        self.pushButton_2.clicked.connect(self.ekip)
        self.pushButton_3.clicked.connect(self.zhrnl)
        self.pushButton_4.clicked.connect(self.exite)
        self.pushButton_6.clicked.connect(self.registr)

        self.action_11.triggered.connect(self.oprog)
        self.action_13.triggered.connect(self.avtor)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "СТРАЖИ ГАЛАКТИКИ"))
        self.pushButton.setText(_translate("MainWindow", "Сотрудники"))
        self.pushButton_2.setText(_translate("MainWindow", "Экипажи"))
        self.pushButton_3.setText(_translate("MainWindow", "Журнал вызовов"))
        self.pushButton_4.setText(_translate("MainWindow", "Выход"))
        self.pushButton_6.setText(_translate("MainWindow", "Вход"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.action.setText(_translate("MainWindow", "О Программе"))
        self.action_2.setText(_translate("MainWindow", "Инструкция"))
        self.action_3.setText(_translate("MainWindow", "Об Авторе"))
        self.action_11.setText(_translate("MainWindow", "О Программе"))
        self.action_13.setText(_translate("MainWindow", "Об Авторе"))
        self.lineEdit_8.setText(_translate("MainWindow", "Login"))
        self.lineEdit_9.setText(_translate("MainWindow", "Password"))

    def exite(self):
        sys.exit()

    def oprog(self):
         QtWidgets.QMessageBox.warning(MainWindow, "О программе.",
                "Программа предназначена для администрирования базы данных организации 'РОСГВАРДИЯ'")

    def avtor(self):
        QtWidgets.QMessageBox.warning(MainWindow, "Об авторе.",
                "Курсант Троицкого Авиационного Технического колледжа - Филиала Московского Государственного Технического \nУниверситета Гражданской Авиации \nГруппы № 432 очной формы обучения \nСпециальность: 'Программирование в компьютерных системах' - \nЖабакова Джамиля Сержановна")

    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
