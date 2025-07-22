

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_registerWindow(object):
    def setupUi(self, registerWindow):
        registerWindow.setObjectName("registerWindow")
        registerWindow.resize(1200, 800)
        registerWindow.setMinimumSize(QtCore.QSize(1200, 800))
        registerWindow.setMaximumSize(QtCore.QSize(1200, 800))
        self.textEdit = QtWidgets.QTextEdit(registerWindow)
        self.textEdit.setGeometry(QtCore.QRect(450, 390, 371, 71))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(registerWindow)
        self.textEdit_2.setGeometry(QtCore.QRect(450, 510, 371, 71))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(registerWindow)
        self.label.setGeometry(QtCore.QRect(290, 400, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(registerWindow)
        self.label_2.setGeometry(QtCore.QRect(290, 520, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(registerWindow)
        self.pushButton.setGeometry(QtCore.QRect(570, 610, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(registerWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(1108, 0, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(registerWindow)
        QtCore.QMetaObject.connectSlotsByName(registerWindow)

    def retranslateUi(self, registerWindow):
        _translate = QtCore.QCoreApplication.translate
        registerWindow.setWindowTitle(_translate("registerWindow", "Form"))
        self.label.setText(_translate("registerWindow", "username"))
        self.label_2.setText(_translate("registerWindow", "password"))
        self.pushButton.setText(_translate("registerWindow", "Register"))
        self.pushButton_4.setText(_translate("registerWindow", "exit"))
