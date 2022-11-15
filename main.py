import sys
import sqlite3

from PyQt5 import uic, QtWidgets, QtCore, QtGui, QtSql
from PyQt5.QtWidgets import QApplication, QMessageBox, QSpinBox, QPushButton
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTextEdit, QLabel


class EditWindow(QMainWindow):
    tableWidget: QtWidgets.QTableWidget
    tableView: QtWidgets.QTableView

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        # self.qdb = QtSql.QSqlDatabase('QSQLITE')
        # self.qdb.setDatabaseName('coffee.sqlite')
        # self.qdb.open()

        # self.model = QtSql.QSqlTableModel(self, self.qdb)
        # self.refresh_view()
        self.update()
        self.save_btn.clicked.connect(self.save)
        self.add_btn.clicked.connect(self.add)
        self.tableWidget.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def update(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute('''SELECT
                        kind_name AS 'Название сорта',
                        roast_level AS 'Степень обжарки 1-10',
                        ground AS 'Молотый / в зернах',
                        flavor_description AS 'Описание вкуса',
                        price AS 'Цена',
                        volume AS 'Объем упаковки'
                        FROM coffee''').fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        print(cur.description)
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def save(self):
        if self.modified:
            cur = self.con.cursor()
            # for
            self.con.commit()
            self.modified.clear()

    def add(self):
        self.cur.execute('INSERT INTO coffee DEFAULT VALUES')
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    # def refresh_view(self):
    #     self.model.setQuery(self.qdb.exec('''SELECT
    #                     kind_name AS 'Название сорта',
    #                     roast_level AS 'Степень обжарки 1-10',
    #                     ground AS 'Молотый / в зернах',
    #                     flavor_description AS 'Описание вкуса',
    #                     price AS 'Цена',
    #                     volume AS 'Объем упаковки'
    #                     FROM coffee'''))
    #     self.tableView.setModel(self.model)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.edit_action = QtWidgets.QAction('Редактировать', self)
        self.menuBar().addAction(self.edit_action)
        self.edit_action.triggered.connect(self.open_edit_window)

        self.con = sqlite3.connect('coffee.sqlite')

        self.qdb = QtSql.QSqlDatabase('QSQLITE')
        self.qdb.setDatabaseName('coffee.sqlite')
        self.qdb.open()

        self.model = QtSql.QSqlTableModel(self, self.qdb)
        self.refresh_view()

    def open_edit_window(self, event):
        ew = EditWindow(self)
        ew.show()


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
