
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QLineEdit, QDialog, QStackedWidget, QMainWindow
from adminWindow import adminWindow
from customerWindow import customerWindow
from loginWindow import loginWindow
from auditWindow import auditWindow
from dbmanager import DBmanager


class PageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pages = {}
        self.stacked_widget = QStackedWidget(self)
        self.init_pages()
        self.setCentralWidget(self.stacked_widget)

    def init_pages(self):
        self.register_page("admin", adminWindow)
        self.register_page("customer", customerWindow)
        self.register_page("login", loginWindow)
        self.register_page("audit", auditWindow)
        self.switch_page("login")

    def register_page(self, name, page_class):
        page = page_class(self.switch_page, self)
        self.pages[name] = page
        self.stacked_widget.addWidget(page)

    def switch_page(self, name):
        print(f"Attempting to switch to page: {name}")
        page = self.pages.get(name)
        if page:
            self.stacked_widget.setCurrentWidget(page)


class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.createDatabase()

    def createDatabase(self):
        self.conn = sqlite3.connect('management.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        self.conn.commit()

    def loadDataFromDatabase(self):
        self.tableWidget.setRowCount(0)  # 清空表格内容
        self.cur.execute("SELECT * FROM users")
        data = self.cur.fetchall()
        for row, (id, name, age) in enumerate(data):
            self.addRow(row, id, name, age)

    def addRow(self, row, id, name, age):
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(id)))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(age)))

    def addRecord(self):
        self.cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("", 0))
        self.conn.commit()
        self.loadDataFromDatabase()

    def addUser(self):
        self.cur.execute("INSERT INTO users (user, password, perm) VALUES (?, ?, ?)", ("", 0, 0))
        self.conn.commit()
        self.loadDataFromDatabase()

    def deleteRecord(self):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            id = self.tableWidget.item(current_row, 0).text()
            self.cur.execute("DELETE FROM users WHERE id=?", (id,))
            self.conn.commit()
            self.loadDataFromDatabase()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to delete.")

    def updateRecord(self):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            id = self.tableWidget.item(current_row, 0).text()
            name = self.tableWidget.item(current_row, 1).text()
            age = self.tableWidget.item(current_row, 2).text()
            self.cur.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, age, id))
            self.conn.commit()
            QMessageBox.information(self, "Update", f"ID: {id}, Name: {name}, Age: {age}")
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to update.")

    def searchData(self):
        keyword = self.searchInput.text()
        self.cur.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + keyword + '%',))
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)  # 清空表格内容
        for row, (id, name, age) in enumerate(data):
            self.addRow(row, id, name, age)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.customerManager.close_connection()
            QApplication.quit()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tableApp = PageManager()

    db_manager = DBmanager()
    db_manager.addUser('admin', 'admin', 1)
    db_manager.addUser('audit', 'audit', 2)
    db_manager.addUserInfo('1', '222', '222')

    tableApp.show()
    sys.exit(app.exec_())
