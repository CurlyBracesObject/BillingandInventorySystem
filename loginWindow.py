
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from dbmanager import DBmanager,current_prem
import config
class loginWindow(QWidget):
    def __init__(self, switch_page, parent=None):
        super(loginWindow, self).__init__(parent)
        self.ui = Ui_loginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.logIN)
        self.db_manager = DBmanager()
        self.switch_page = switch_page

    def logIN(self):
        username = self.ui.textEdit.toPlainText().strip()
        password = self.ui.textEdit_2.toPlainText().strip()

        Admin_info = self.db_manager.loadDataFromAdmin()
        User_info = self.db_manager.loadDataFromUser()

        # Debug
        print(f"Username: {username}, Password: {password}")

        for admin_info in Admin_info:
            db_username, db_password, perm = admin_info[1], admin_info[2], admin_info[3]
            print(f"Checking admin: {db_username}, {db_password}, perm: {perm}")
            if username == db_username and password == db_password:
                if perm == 1:
                    config.current_prem = perm
                    print("Prem is", config.current_prem)
                    self.switch_page("admin")
                    return
                elif perm == 2:
                    config.current_prem = perm
                    print("Prem is", config.current_prem)
                    self.switch_page("audit")
                    return

        for user_info in User_info:
            print(f"Checking user: {user_info}")
            C_username, C_password = user_info[5], user_info[6]  # 确保索引正确
            if username == C_username and password == C_password:
                config.current_user_id = user_info[1]  # 确保这里的索引是用户ID字段
                print("User ID:", config.current_user_id)
                self.switch_page("customer")
                return

        QMessageBox.warning(self, "Login", "Invalid username or password.")



class Ui_loginWindow(object):
    def setupUi(self, loginWindow):
        loginWindow.setObjectName("loginWindow")
        loginWindow.resize(1600, 900)
        loginWindow.setMinimumSize(QtCore.QSize(1600, 900))
        loginWindow.setMaximumSize(QtCore.QSize(1600, 900))

        # 设置用户名标签的位置和大小
        self.label = QtWidgets.QLabel(loginWindow)
        self.label.setGeometry(QtCore.QRect(500, 300, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)#将字体应用到标签
        self.label.setObjectName("label")

        # 设置用户名文本框的位置和大小
        self.textEdit = QtWidgets.QTextEdit(loginWindow)
        self.textEdit.setGeometry(QtCore.QRect(700, 300, 400, 50))
        self.textEdit.setObjectName("textEdit")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.textEdit.setFont(font)  # 设置字体和大小

        # 设置密码标签的位置和大小
        self.label_2 = QtWidgets.QLabel(loginWindow)
        self.label_2.setGeometry(QtCore.QRect(500, 400, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # 设置密码文本框的位置和大小
        self.textEdit_2 = QtWidgets.QTextEdit(loginWindow)
        self.textEdit_2.setGeometry(QtCore.QRect(700, 400, 400, 50))
        self.textEdit_2.setObjectName("textEdit_2")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.textEdit_2.setFont(font)  # 设置字体和大小

        # 设置登录按钮的位置和大小
        self.pushButton_2 = QtWidgets.QPushButton(loginWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(850, 500, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(loginWindow)#cccc
        QtCore.QMetaObject.connectSlotsByName(loginWindow)#ccc

    def retranslateUi(self, loginWindow):
        _translate = QtCore.QCoreApplication.translate
        loginWindow.setWindowTitle(_translate("loginWindow", "Form"))
        self.label.setText(_translate("loginWindow", "username"))
        self.label_2.setText(_translate("loginWindow", "password"))
        self.pushButton_2.setText(_translate("loginWindow", "LogIn"))








