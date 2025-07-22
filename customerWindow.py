
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, \
    QMessageBox, QApplication, QInputDialog, QLineEdit, QSpinBox, QDialog, QComboBox
from dbmanager import DatabaseManager
import config
class customerWindow(QWidget):
    def __init__(self, switch_page, parent =None):
        super(customerWindow, self).__init__(parent)

        self.ui = Ui_customerWindow()
        self.ui.setupUi(self)
        self.bind_main_buttons()
        self.customerManager = DatabaseManager(self.ui.tableWidget)
        self.ui.textEdit.textChanged.connect(self.search_data)
        self.customerManager.connect_to_db('management.db')
        self.ui.pushButton_4.clicked.connect(self.close_window)
        self.ui.payButton_2.clicked.connect(self.show_bills_to_pay)
        self.status = None
    def bind_main_buttons(self):
        self.ui.billButton.clicked.connect(lambda: self.update_status_and_load_table(
            'management.db',
            'bill_info',
            ['bill_id', 'bill_customer_id', 'bill_type', 'bill_receipt', 'bill_description', 'bill_amount', 'unpaid_bill'],
            {'bill_customer_id': config.current_user_id},
            'bill'
        ))
        self.ui.transactionButton.clicked.connect(lambda: self.update_status_and_load_table(
            'management.db',
            'transaction_info',
            [
                'transaction_id','transaction_customer_id', 'transaction_amount', 'transaction_bill','transaction_number',
                'transaction_type', 'transaction_history', 'transaction_description'
            ],
            {'transaction_customer_id': config.current_user_id},
            'transaction'
        ))

        self.ui.pushButton_4.clicked.connect(self.close)

    def bind_crud_buttons(self):

        self.ui.addButton.clicked.connect(self.add_row)
        self.ui.delButton.clicked.connect(self.delete_record)
        self.ui.pushButton_10.clicked.connect(self.update_record)

    def update_status_and_load_table(self, db_path, table_name, columns, filters, status):
        self.status = status
        print("status is", self.status)
        self.load_table_data(db_path, table_name, columns, filters)

    def load_table_data(self, db_path, table_name, columns, filters=None):
        self.current_db_path = db_path
        self.current_table = table_name
        self.current_columns = columns
        self.customerManager.connect_to_db(db_path)
        self.customerManager.loadDataFromDatabase(table_name, columns, filters)
        print("current_id is",config.current_user_id)
        print(filters)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(columns)

    def add_row(self):
        self.customerManager.addEmptyRow()

    def delete_record(self):
        if self.current_table:
            self.customerManager.deleteRecord(self.current_table, self.current_columns[0])

    def update_record(self):
        if self.current_table and self.current_columns:
            self.customerManager.updateRecord(self.current_table, self.current_columns[0], self.current_columns)

    @pyqtSlot()
    def search_data(self):
        if self.current_table and self.current_columns:
            keyword = self.ui.textEdit.toPlainText()
            selected_column = self.ui.comboBox.currentIndex()

            # Debug information
            print(f"Selected column index: {selected_column}, column name: {self.current_columns[selected_column]}")

            # Assuming you have a method `getFilters` that retrieves the filter conditions from the UI
            filters = self.getFilters()

            # Pass the filters to the searchData method
            self.customerManager.searchData(self.current_table, self.current_columns[selected_column], keyword, filters)

    def getFilters(self):
        filters = {}
        if self.status == 'bill':
            filters['bill_customer_id'] = config.current_user_id
        elif self.status == 'transaction':
            filters['transaction_customer_id'] = config.current_user_id
        print("filters is", filters)
        return filters

    def close_window(self):

        event = QCloseEvent()
        self.closeEvent(event)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.customerManager.close_connection()
            QApplication.quit()
        else:
            event.ignore()

    def show_bills_to_pay(self):
        bills = self.customerManager.get_bills_to_pay(config.current_user_id)
        if not bills:
            QMessageBox.warning(self, "No Bill to Pay", "No bill to pay for this customer.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Bills to Pay")
        layout = QVBoxLayout()
        bill_selector_label = QLabel("Select a bill to pay:")
        layout.addWidget(bill_selector_label)

        bill_selector = QComboBox()
        bill_dict = {}
        for bill in bills:
            bill_id, bill_amount, unpaid = bill
            bill_amount = float(bill_amount)  # 转换为浮点数
            unpaid = float(unpaid)  # 转换为浮点数
            amount_due = bill_amount - unpaid
            bill_desc = f"Bill ID: {bill_id}, Amount Due: {amount_due}, Unpaid: {unpaid}"
            bill_selector.addItem(bill_desc, bill_id)
            bill_dict[bill_id] = (bill_amount, unpaid)
        layout.addWidget(bill_selector)


        amount_label = QLabel("Enter amount to pay:")
        amount_input = QSpinBox()
        amount_input.setMaximum(1000000)
        layout.addWidget(amount_label)
        layout.addWidget(amount_input)


        button = QPushButton("Pay")
        layout.addWidget(button)
        button.clicked.connect(lambda: self.process_payment(bill_selector.currentData(), amount_input.value(), bill_dict))
        dialog.setLayout(layout)
        dialog.exec_()

    def process_payment(self, bill_id, amount, bill_dict):
        bill_amount, unpaid = bill_dict[bill_id]
        if amount <= bill_amount:

            new_unpaid = unpaid - amount
            # Update unpaid_bill in bill_info table
            update_query_bill_info = "UPDATE bill_info SET unpaid_bill = ? WHERE bill_id = ?"
            self.customerManager.cur.execute(update_query_bill_info, (new_unpaid, bill_id))

            # Update transaction_history_bill in transaction_history_info table
            update_query_transaction_history = "UPDATE transaction_history_info SET transaction_history_bill = ? WHERE transaction_history_id = ?"
            self.customerManager.cur.execute(update_query_transaction_history, (new_unpaid, bill_id))

            # Commit the changes
            self.customerManager.conn.commit()

            QMessageBox.information(None, "Payment Processed",
                                    f"Payment of {amount} has been processed. New unpaid amount: {new_unpaid}")
        else:
            QMessageBox.warning(None, "Payment Error", "Amount exceeds the bill amount.")



class Ui_customerWindow(object):
    def setupUi(self, customerWindow):
        customerWindow.setObjectName("customerWindow")
        customerWindow.resize(1200, 800)
        customerWindow.setMinimumSize(QtCore.QSize(1200, 800))
        customerWindow.setMaximumSize(QtCore.QSize(1200, 800))

        self.tableWidget = QtWidgets.QTableWidget(customerWindow)
        self.tableWidget.setGeometry(QtCore.QRect(300, 110, 891, 541))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.verticalLayoutWidget = QtWidgets.QWidget(customerWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 110, 291, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.billButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.billButton.setFont(font)
        self.billButton.setObjectName("billButton")
        self.billButton.setMinimumSize(QtCore.QSize(0, 60))
        self.verticalLayout.addWidget(self.billButton)

        self.transactionButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.transactionButton.setFont(font)
        self.transactionButton.setObjectName("transactionButton")
        self.transactionButton.setMinimumSize(QtCore.QSize(0, 60))
        self.verticalLayout.addWidget(self.transactionButton)

        self.pushButton_4 = QtWidgets.QPushButton(customerWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(1108, 0, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.textEdit = QtWidgets.QLineEdit(customerWindow)  # Using QLineEdit
        self.textEdit.setGeometry(QtCore.QRect(430, 70, 641, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)  # Adjusting font size
        self.textEdit.setFont(font)
        self.textEdit.setPlaceholderText("Enter search text here...")  # Adding placeholder text
        self.textEdit.setAlignment(QtCore.Qt.AlignLeft)  # Aligning text to the left
        self.textEdit.setObjectName("textEdit")

        self.comboBox = QtWidgets.QComboBox(customerWindow)
        self.comboBox.setGeometry(QtCore.QRect(1090, 70, 100, 31))
        self.comboBox.setObjectName("comboBox")

        self.label = QtWidgets.QLabel(customerWindow)
        self.label.setGeometry(QtCore.QRect(330, 70, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.payButton_2 = QtWidgets.QPushButton(customerWindow)
        self.payButton_2.setGeometry(QtCore.QRect(600, 680, 289, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.payButton_2.setFont(font)
        self.payButton_2.setObjectName("payButton_2")

        self.retranslateUi(customerWindow)
        QtCore.QMetaObject.connectSlotsByName(customerWindow)

    def retranslateUi(self, customerWindow):
        _translate = QtCore.QCoreApplication.translate
        customerWindow.setWindowTitle(_translate("customerWindow", "Form"))
        self.billButton.setText(_translate("customerWindow", "Bill Check"))
        self.transactionButton.setText(_translate("customerWindow", "Transaction Check"))
        self.pushButton_4.setText(_translate("customerWindow", "Exit"))
        self.label.setText(_translate("customerWindow", "Search"))
        self.payButton_2.setText(_translate("customerWindow", "Pay"))






