import random
import sys
import sqlite3
import os
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QInputDialog, QSpinBox, QLineEdit, \
    QComboBox, QPushButton, QMessageBox, QSplashScreen, QStyledItemDelegate, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class DialogAddFilm(QDialog):
    def __init__(self, variety, roasting, fraction, description, sell, volume):
        super().__init__()
        label_name = QLabel('Введите название кофе')
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.setWindowTitle("Добавить кофе")
        label_variety = QLabel("Введите название сорта")
        self.varietyInp = QLineEdit()
        label_roasting = QLabel("Введите степень обжарки")
        self.roastingInp = QLineEdit()
        label_fraction = QLabel("Введите фракцию(молотый/в зернах)")
        self.fractionInp = QLineEdit()
        label_description = QLabel("Введите описание вкуса")
        self.descriptionInp = QLineEdit()
        label_sell = QLabel("Введите цену")
        self.sellInp = QSpinBox()
        self.sellInp.setMaximum(10000)
        self.sellInp.setMinimum(150)
        label_volume = QLabel("Введите объем упаковки")
        self.volumeInp = QSpinBox()
        self.volumeInp.setMaximum(10000)
        self.volumeInp.setMinimum(10)
        self.varietyInp.setText(variety)
        self.roastingInp.setText(roasting)
        self.fractionInp.setText(fraction)
        self.descriptionInp.setText(description)
        self.sellInp.setValue(int(sell))
        self.volumeInp.setValue(int(volume))
        self.layout.addWidget(label_variety)
        self.layout.addWidget(self.varietyInp)
        self.layout.addWidget(label_roasting)
        self.layout.addWidget(self.roastingInp)
        self.layout.addWidget(label_fraction)
        self.layout.addWidget(self.fractionInp)
        self.layout.addWidget(label_description)
        self.layout.addWidget(self.descriptionInp)
        self.layout.addWidget(label_sell)
        self.layout.addWidget(self.sellInp)
        self.layout.addWidget(label_volume)
        self.layout.addWidget(self.volumeInp)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)
        self.con = sqlite3.connect('Data/coffee.sqlite')
        self.open_tableFilms()
        self.popbtn.clicked.connect(self.deleteRowFilms)
        self.addbtn.clicked.connect(self.add_tableRowFilms)
        self.editbtn.clicked.connect(self.edit_tableFilms)

    def open_tableFilms(self):
        name = 'coffee'
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM {name}").fetchall()
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                item = QTableWidgetItem(str(val))
                self.table.setItem(i, j, item)
        self.table.setHorizontalHeaderLabels(['ID',
                                              'variety',
                                              'roasting',
                                              'fraction',
                                              'description',
                                              'sell',
                                              'volume'])

    def deleteRowFilms(self):
        name = 'coffee'
        row = self.table.currentRow()
        if row != -1:
            data = []
            for col in range(7):
                data.append(self.table.item(row, col).text())
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM {name} WHERE ID='{data[0]}' AND "
                        f"variety='{data[1]}' AND "
                        f"roasting='{data[2]}' AND "
                        f"fraction='{data[3]}' AND "
                        f"description='{data[4]}' AND "
                        f"sell={data[5]} AND "
                        f"volume={data[6]}")
            self.con.commit()
            self.open_tableFilms()
        else:
            self.statusbar.showMessage('ERROR')

    def add_tableRowFilms(self, n, variety='', roasting='', fraction='', description='', sell=150, volume='10'):
        cur = self.con.cursor()
        dlg = DialogAddFilm(variety, roasting, fraction, description, sell, volume)
        if dlg.exec():
            cur.execute(f"INSERT INTO coffee(ID, variety, roasting, fraction, description, sell, volume) "
                        f"VALUES("
                        f"'{random.randrange(0, 99999999)}',"
                        f"'{dlg.varietyInp.text()}',"
                        f"'{dlg.roastingInp.text()}',"
                        f"'{dlg.fractionInp.text()}',"
                        f"'{dlg.descriptionInp.text()}',"
                        f"{dlg.sellInp.value()},"
                        f"{dlg.volumeInp.value()})")
            self.con.commit()
            self.open_tableFilms()

    def edit_tableFilms(self):
        row = self.table.currentRow()
        if row != -1:
            data = []
            for col in range(7):
                data.append(self.table.item(row, col).text())
            cur = self.con.cursor()
            dlg = DialogAddFilm(data[1], data[2], data[3], data[4], data[5], data[6])
            if dlg.exec():
                cur.execute(f"UPDATE coffee SET "
                            f"variety='{dlg.varietyInp.text()}', "
                            f"roasting='{dlg.roastingInp.text()}', "
                            f"fraction='{dlg.fractionInp.text()}', "
                            f"description='{dlg.descriptionInp.text()}', "
                            f"sell={dlg.sellInp.value()}, "
                            f"volume={dlg.volumeInp.value()} WHERE id={data[0]}")
                self.con.commit()
                self.open_tableFilms()
        else:
            self.statusbar.showMessage('ERROR')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
