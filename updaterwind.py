# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updater.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UpdaterWindow(object):
    def setupUi(self, UpdaterWindow):
        UpdaterWindow.setObjectName("UpdaterWindow")
        UpdaterWindow.setFixedSize(742, 457)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        UpdaterWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(UpdaterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 340, 81, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 340, 81, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 10, 491, 51))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 60, 381, 41))
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(130, 110, 481, 192))
        self.textBrowser.setObjectName("textBrowser")
        UpdaterWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UpdaterWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 742, 22))
        self.menubar.setObjectName("menubar")
        UpdaterWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UpdaterWindow)
        self.statusbar.setObjectName("statusbar")
        UpdaterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(UpdaterWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdaterWindow)

    def retranslateUi(self, UpdaterWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdaterWindow.setWindowTitle(_translate("UpdaterWindow", "Updater"))
        self.pushButton.setText(_translate("UpdaterWindow", "Да"))
        self.pushButton_2.setText(_translate("UpdaterWindow", "Нет"))
        self.label.setText(_translate("UpdaterWindow", "Вышло новое обновление лаунчера. Хотите его обновить?"))
        self.label_2.setText(_translate("UpdaterWindow", "Список изменений"))
        self.textBrowser.setHtml(_translate("UpdaterWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))