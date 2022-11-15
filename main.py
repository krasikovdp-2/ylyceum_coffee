import sys
import sqlite3

from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtSql
from PyQt5.QtWidgets import QApplication, QMessageBox, QSpinBox, QPushButton
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTextEdit, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.con = sqlite3.connect('coffee.sqlite')

        self.qdb = QtSql.QSqlDatabase('QSQLITE')
        self.qdb.setDatabaseName('coffee.sqlite')
        self.qdb.open()

        self.model = QtSql.QSqlTableModel(self, self.qdb)
        self.refresh_view()

    def refresh_view(self):
        self.model.setQuery(self.qdb.exec('''SELECT
                kind_name AS 'Название сорта',
                roast_level AS 'Степень обжарки 1-10',
                ground AS 'Молотый / в зернах',
                flavor_description AS 'Описание вкуса',
                price AS 'Цена',
                volume AS 'Объем упаковки'
                FROM coffee'''))
        self.tableView.setModel(self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
