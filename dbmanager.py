
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import pandas as pd
current_user_id = None
current_prem = None
DATABASE_PATH = 'C:\\Users\\XUE\\Desktop\\cps3320\\cps3320project_revise\\management.db'
class DBmanager:
    def __init__(self):
        self.createDatabase()

    def createDatabase(self):
        # 创建数据库连接并创建表格
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY, user TEXT, password TEXT, perm INTEGER)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user_info
                            (id INTEGER PRIMARY KEY, customer_id TEXT, customer_name TEXT, customer_mobile TEXT,
                             customer_email TEXT, customer_username TEXT, customer_password TEXT, customer_address TEXT)''')
        self.conn.commit()

    def addUser(self, name, password, perm):
        self.cur.execute("INSERT INTO users (user, password, perm) VALUES (?, ?, ?)", (name, password, perm))
        self.conn.commit()
        return self.cur.lastrowid

    def addUserInfo(self, customer_id, name, password):
        self.cur.execute("INSERT INTO user_info (customer_id, customer_username, customer_password) VALUES (?, ?, ?)", (customer_id, name, password))
        self.conn.commit()

    def loadDataFromAdmin(self):
        self.cur.execute("SELECT * FROM users")
        data = self.cur.fetchall()
        return data

    def loadDataFromUser(self):
        self.cur.execute("SELECT * FROM user_info")
        data = self.cur.fetchall()
        print(f"Loaded user info: {data}")  # 添加调试信息
        return data


class DatabaseManager:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.conn = None
        self.cur = None
    def connect_to_db(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def loadDataFromDatabase(self, table_name, columns, filters=None):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)


        all_columns = ["id"] + columns


        query = f"SELECT {', '.join(all_columns)} FROM {table_name}"


        if filters:
            filter_conditions = []
            for key, value in filters.items():
                filter_conditions.append(f"{key} = '{value}'")
            filter_clause = " AND ".join(filter_conditions)
            query += f" WHERE {filter_clause}"

        self.cur.execute(query)
        data = self.cur.fetchall()

        for row, record in enumerate(data):
            self.addRow(row, record[1:])
        self.adjustColumnWidths()

    def addRow(self, row, record):
        self.tableWidget.insertRow(row)
        for col, value in enumerate(record):
            self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def addEmptyRow(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(row_position, col, QTableWidgetItem(""))

    def addRecord(self, table_name, column_names, values):
        columns_str = ', '.join(column_names)
        placeholders = ', '.join('?' * len(values))
        self.cur.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", values)
        self.conn.commit()
        self.loadDataFromDatabase(table_name, column_names)

    def deleteRecord(self, table_name, id_column):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:
            id_value = self.tableWidget.item(current_row, 0).text()
            self.cur.execute(f"DELETE FROM {table_name} WHERE {id_column}=?", (id_value,))
            self.conn.commit()
            self.tableWidget.removeRow(current_row)
        else:
            QMessageBox.warning(self.tableWidget, "Warning", "Please select a row to delete.")

    def updateRecord(self, table_name, id_column, columns):
        current_row = self.tableWidget.currentRow()
        if current_row != -1:

            values = [self.tableWidget.item(current_row, col).text() for col in range(len(columns))]

            query = f"SELECT id FROM {table_name} WHERE {columns[0]} = ?"
            self.cur.execute(query, (self.tableWidget.item(current_row, 0).text(),))
            result = self.cur.fetchone()

            if result:
                id_value = result[0]
                set_clause = ', '.join(f"{col}=?" for col in columns)
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE id=?"
                self.cur.execute(update_query, (*values, id_value))
            else:
                columns_str = ', '.join(columns)
                placeholders = ', '.join('?' * len(values))
                insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                self.cur.execute(insert_query, values)

            # 更新 transaction_history_info 表
            if table_name == 'bill_info':
                print(values)
                transaction_history_data = {
                    'transaction_history_id': values[0],
                    'transaction_history_customer_id': values[1],  # 使用 bill_info 的某些字段更新 transaction_history_info
                    'transaction_history_amount': values[6],
                    'transaction_history_bill': values[6],  # 假设 bill_info 的第 7 列是未支付的账单信息
                    'transaction_history_number': values[2],  # 假设 bill_info 的第 3 列是账单号
                    'transaction_history_type': values[3],  # 假设 bill_info 的第 4 列是账单类型
                    'transaction_history_description': values[5]  # 假设 bill_info 的第 6 列是账单描述
                }
                self.cur.execute(
                    "INSERT INTO transaction_history_info (transaction_history_id, transaction_history_customer_id, transaction_history_amount, transaction_history_bill, transaction_history_number, transaction_history_type, transaction_history_description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (transaction_history_data['transaction_history_id'],
                     transaction_history_data['transaction_history_customer_id'],
                     transaction_history_data['transaction_history_amount'],
                     transaction_history_data['transaction_history_bill'],
                     transaction_history_data['transaction_history_number'],
                     transaction_history_data['transaction_history_type'],
                     transaction_history_data['transaction_history_description']))

            self.conn.commit()
            self.loadDataFromDatabase(table_name, columns)
            QMessageBox.information(self.tableWidget, "Update", "Record updated successfully.")
        else:
            QMessageBox.warning(self.tableWidget, "Warning", "Please select a row to update.")

    def searchData(self, table_name, search_column, keyword, filters=None):
        print(f"Searching in table: {table_name}, column: {search_column}, for keyword: {keyword}")  # Debug information

        query = f"SELECT {', '.join(self.exclude_id_column(table_name))} FROM {table_name} WHERE {search_column} LIKE ?"
        params = ['%' + keyword + '%']

        # If filters are provided, add them to the query
        if filters:
            for filter_column, filter_value in filters.items():
                query += f" AND {filter_column} = ?"
                params.append(filter_value)

        print(f"Query: {query}, Params: {params}")  # Debug information
        self.cur.execute(query, params)
        data = self.cur.fetchall()
        print(f"Search results: {data}")
        self.tableWidget.setRowCount(0)
        for row, record in enumerate(data):
            self.addRow(row, record)
        self.adjustColumnWidths()

    def exclude_id_column(self, table_name):
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns_info = self.cur.fetchall()
        return [info[1] for info in columns_info if info[1] != 'id']

    def adjustColumnWidths(self):

        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, 180)

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def get_bills_to_pay(self, bill_customer_id):

        query = "SELECT bill_id, bill_amount, unpaid_bill FROM bill_info WHERE bill_customer_id = ? AND (unpaid_bill - bill_amount) <= 0"
        self.cur.execute(query, (bill_customer_id,))
        return self.cur.fetchall()

    def process_payment(self, bill_id, amount):

        query = "SELECT bill_amount, unpaid_bill FROM bill_info WHERE bill_id = ?"
        self.cur.execute(query, (bill_id,))
        result = self.cur.fetchone()

        if result:
            bill_amount, unpaid = result
            bill_amount = float(bill_amount)
            unpaid = float(unpaid)
            amount = float(amount)

            if unpaid + amount <= bill_amount:

                new_unpaid = amount - unpaid
                update_query = "UPDATE bill_info SET unpaid_bill = ? WHERE bill_id = ?"
                self.cur.execute(update_query, (new_unpaid, bill_id))
                self.conn.commit()
                QMessageBox.information(None, "Payment Processed",
                                        f"Payment of {amount} has been processed. New unpaid amount: {new_unpaid}")
            else:
                QMessageBox.warning(None, "Payment Error", "Amount exceeds the bill amount.")
        else:
            QMessageBox.warning(None, "Payment Error", "Bill ID not found.")

    def loadAllData(self):
        tables = {
            'bill_info': ['bill_id', 'bill_customer_id', 'bill_number', 'bill_type', 'bill_receipt', 'bill_description',
                          'bill_amount', 'unpaid_bill'],
            'transaction_info': ['transaction_id', 'transaction_customer_id', 'transaction_amount', 'transaction_bill',
                                 'transaction_number', 'transaction_type', 'transaction_history',
                                 'transaction_description'],
            'user_info': ['customer_id', 'customer_name', 'customer_mobile', 'customer_email', 'customer_username',
                          'customer_password', 'customer_address']
        }

        all_data = {}
        for table, columns in tables.items():
            query = f"SELECT {', '.join(columns)} FROM {table}"
            self.cur.execute(query)
            data = self.cur.fetchall()
            all_data[table] = (columns, data)

        return all_data

    def write_to_excel(self, file_path):
        all_data = self.loadAllData()
        with pd.ExcelWriter(file_path) as writer:
            for table_name, (columns, data) in all_data.items():
                df = pd.DataFrame(data, columns=columns)
                df.to_excel(writer, sheet_name=table_name, index=False)
        QMessageBox.information(None, "Excel Export", f"Data successfully exported to {file_path}")
