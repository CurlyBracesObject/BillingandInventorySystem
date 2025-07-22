from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, \
    QMessageBox, QApplication, QFileDialog
from dbmanager import DatabaseManager,DBmanager
import config
class adminWindow(QWidget):
    def __init__(self, switch_page, parent=None):
        super(adminWindow, self).__init__(parent)
        self.ui = Ui_adminWindow()
        self.ui.setupUi(self)
        self.adminManager = DatabaseManager(self.ui.tableWidget)
        self.current_table = None
        self.current_columns = None
        self.current_db_path = None
        self.current_db_path = 'management.db'
        self.connect_to_db()
        self.bind_main_buttons()
        self.bind_crud_buttons()

        self.ui.textEdit.textChanged.connect(self.search_data)

    def bind_main_buttons(self):

        self.ui.pushButton_3.clicked.connect(lambda: self.load_table_data('management.db', 'user_info', ['customer_id', 'customer_name', 'customer_mobile','customer_email','customer_username','customer_password','customer_address']))
        self.ui.pushButton_5.clicked.connect(lambda: self.load_table_data('management.db', 'transaction_info', [
            'transaction_id','transaction_customer_id', 'transaction_amount', 'transaction_bill',
            'transaction_number', 'transaction_type', 'transaction_history', 'transaction_description'
        ]))
        self.ui.pushButton.clicked.connect(lambda: self.load_table_data('management.db', 'bill_info', ['bill_id', 'bill_customer_id', 'bill_number','bill_type','bill_receipt','bill_description','bill_amount','unpaid_bill']))
        self.ui.pushButton_2.clicked.connect(lambda: self.load_table_data('management.db', 'payment_info', ['payment_id', 'payment_customer_id', 'payment_des','payment_status']))
        self.ui.pushButton_6.clicked.connect(lambda: self.load_table_data('management.db', 'transaction_history_info', ['transaction_history_id', 'transaction_history_customer_id', 'transaction_history_amount', 'transaction_history_bill', 'transaction_history_number', 'transaction_history_type', 'transaction_history_description']))
        self.ui.pushButton_7.clicked.connect(self.export_to_excel)
        self.ui.pushButton_4.clicked.connect(self.close_window)

    def connect_to_db(self):
        self.adminManager.connect_to_db(self.current_db_path)
    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.adminManager.write_to_excel(file_path)

    def bind_crud_buttons(self):
        self.ui.addButton.clicked.connect(self.add_row)
        self.ui.delButton.clicked.connect(self.delete_record)
        self.ui.pushButton_10.clicked.connect(self.update_record)

    def load_table_data(self, db_path, table_name, columns):
        self.current_db_path = db_path
        self.current_table = table_name
        self.current_columns = columns
        self.adminManager.connect_to_db(db_path)
        self.adminManager.loadDataFromDatabase(table_name, columns)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(columns)

    def add_row(self):
        self.adminManager.addEmptyRow()
    def delete_record(self):
        if self.current_table:
            self.adminManager.deleteRecord(self.current_table, self.current_columns[0])
    def update_record(self):
        if self.current_table and self.current_columns:
            self.adminManager.updateRecord(self.current_table, self.current_columns[0], self.current_columns)

    @pyqtSlot()
    def search_data(self):
        if self.current_table and self.current_columns:
            keyword = self.ui.textEdit.toPlainText()
            selected_column = self.ui.comboBox.currentIndex()
            print(f"Selected column index: {selected_column}, column name: {self.current_columns[selected_column]}")  # Debug information
            self.adminManager.searchData(self.current_table, self.current_columns[selected_column], keyword)

    def close_window(self):
        event = QCloseEvent()
        self.closeEvent(event)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.adminManager.close_connection()
            QApplication.quit()
        else:
            event.ignore()

class Ui_adminWindow(object):
    def setupUi(self, adminWindow):
        adminWindow.setObjectName("adminWindow")
        adminWindow.resize(1600, 900)  # 调整窗口大小
        adminWindow.setMinimumSize(QtCore.QSize(1600, 900))
        adminWindow.setMaximumSize(QtCore.QSize(1600, 900))

        self.tableWidget = QTableWidget(adminWindow)
        self.tableWidget.setGeometry(QtCore.QRect(350, 150, 1200, 600))  # 调整表格的大小
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.verticalLayoutWidget = QWidget(adminWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 150, 330, 600))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 调整按钮大小和位置
        self.pushButton_3 = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_5 = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_6 = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)

        self.pushButton_4 = QPushButton(adminWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(1450, 10, 120, 50))  # 调整按钮的位置和大小
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        # 调整搜索标签的位置和大小
        self.label = QLabel(adminWindow)
        self.label.setGeometry(QtCore.QRect(350, 70, 150, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # 调整搜索框的位置和大小
        self.textEdit = QTextEdit(adminWindow)
        self.textEdit.setGeometry(QtCore.QRect(510, 70, 600, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.comboBox = QtWidgets.QComboBox(adminWindow)
        self.comboBox.setGeometry(QtCore.QRect(1120, 70, 150, 31))
        self.comboBox.setObjectName("comboBox")

        # 调整底部按钮的位置和大小
        self.addButton = QPushButton(adminWindow)
        self.addButton.setGeometry(QtCore.QRect(450, 800, 120, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")

        self.delButton = QPushButton(adminWindow)
        self.delButton.setGeometry(QtCore.QRect(650, 800, 120, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.delButton.setFont(font)
        self.delButton.setObjectName("delButton")

        self.pushButton_10 = QPushButton(adminWindow)
        self.pushButton_10.setGeometry(QtCore.QRect(850, 800, 120, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")

        self.retranslateUi(adminWindow)
        QtCore.QMetaObject.connectSlotsByName(adminWindow)

    def retranslateUi(self, adminWindow):
        _translate = QtCore.QCoreApplication.translate
        adminWindow.setWindowTitle(_translate("adminWindow", "Admin Panel"))
        self.pushButton_3.setText(_translate("adminWindow", "Customer Management"))
        self.pushButton_5.setText(_translate("adminWindow", "Transaction Management"))
        self.pushButton.setText(_translate("adminWindow", "Bill Management"))
        self.pushButton_2.setText(_translate("adminWindow", "Payment Management"))
        self.pushButton_6.setText(_translate("adminWindow", "Transaction History"))
        self.pushButton_7.setText(_translate("adminWindow", "Report Generation"))
        self.pushButton_4.setText(_translate("adminWindow", "Exit"))
        self.label.setText(_translate("adminWindow", "Search"))
        self.addButton.setText(_translate("adminWindow", "Add"))
        self.delButton.setText(_translate("adminWindow", "Delete"))
        self.pushButton_10.setText(_translate("adminWindow", "Update"))
