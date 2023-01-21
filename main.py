import sys
import sqlite3
import os
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QInputDialog, QSpinBox, QLineEdit, \
    QComboBox, QPushButton, QMessageBox, QSplashScreen, QStyledItemDelegate, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class DialogAddFilm(QDialog):
    def __init__(self, generes, name, year, genre, duration):
        super().__init__()
        label_name = QLabel('Введите название фильма')
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.inp_name = QLineEdit()
        self.setWindowTitle("Добавить фильм")
        label_num = QLabel("Ввдите год выпуска фильма")
        self.inp_num = QSpinBox()
        label_char = QLabel("Выберите жанр фильма")
        label_duration = QLabel("Введите продолжительность фильма")
        self.inp_duration = QSpinBox()
        self.inp_num.setMaximum(10000)
        self.inp_duration.setMaximum(10000)
        self.inp_char = QComboBox()
        self.inp_char.addItems(generes)
        self.inp_name.setText(name)
        self.inp_num.setValue(year)
        self.inp_duration.setValue(duration)
        self.inp_char.setCurrentText(genre)
        self.layout.addWidget(label_name)
        self.layout.addWidget(self.inp_name)
        self.layout.addWidget(label_num)
        self.layout.addWidget(self.inp_num)
        self.layout.addWidget(label_char)
        self.layout.addWidget(self.inp_char)
        self.layout.addWidget(label_duration)
        self.layout.addWidget(self.inp_duration)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.open_tableFilms()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
