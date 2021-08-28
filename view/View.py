# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets
from config.config import launch_name


class Ui_MainWindow():

    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setFixedSize(800, 600)

    def setup_main_window(self):
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.but_play = QtWidgets.QPushButton(self.centralwidget)
        self.but_play.setGeometry(QtCore.QRect(250, 400, 301, 91))
        self.but_play.setObjectName("but_play")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line_username = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_username.setObjectName("line_email")
        self.verticalLayout.addWidget(self.line_username)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.line_password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.line_password.setObjectName("line_password")
        self.verticalLayout.addWidget(self.line_password)
        self.but_login = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.but_login.setObjectName("but_login")
        self.verticalLayout.addWidget(self.but_login)
        self.but_install = QtWidgets.QPushButton(self.centralwidget)
        self.but_install.setGeometry(QtCore.QRect(10, 230, 161, 61))
        self.but_install.setObjectName("but_install")
        self.but_registration = QtWidgets.QPushButton(self.centralwidget)
        self.but_registration.setGeometry(QtCore.QRect(610, 60, 181, 31))
        self.but_registration.setObjectName("but_registration")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(620, 10, 161, 41))
        self.label_3.setObjectName("label_3")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(590, 160, 191, 51))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(650, 110, 141, 41))
        self.label_4.setObjectName("label_4")
        self.lab_installing = QtWidgets.QLabel(self.centralwidget)
        self.lab_installing.setGeometry(QtCore.QRect(10, 310, 201, 71))
        self.lab_installing.setText("")
        self.lab_installing.setObjectName("lab_installing")
        self.lab_memory = QtWidgets.QLabel(self.centralwidget)
        self.lab_memory.setGeometry(QtCore.QRect(590, 210, 67, 17))
        self.lab_memory.setObjectName("lab_memory")
        self.but_exit = QtWidgets.QPushButton(self.centralwidget)
        self.but_exit.setGeometry(QtCore.QRect(680, 10, 111, 41))
        self.but_exit.setDefault(False)
        self.but_exit.setObjectName("but_exit")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(290, 370, 231, 21))
        self.progressBar.setValue(0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.close()

        self.but_send_skin = QtWidgets.QPushButton(self.centralwidget)
        self.but_send_skin.setGeometry(QtCore.QRect(310, 10, 171, 41))
        self.but_send_skin.setObjectName("but_send_skin")
        self.but_send_cape = QtWidgets.QPushButton(self.centralwidget)
        self.but_send_cape.setGeometry(QtCore.QRect(310, 70, 171, 41))
        self.but_send_cape.setObjectName("but_send_cape")

        self.retranslate_main_window()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_main_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", launch_name))
        self.but_play.setText(_translate("MainWindow", "Играть"))
        self.label.setText(_translate("MainWindow", "Имя пользователя"))
        self.label_2.setText(_translate("MainWindow", "Пароль"))
        self.but_login.setText(_translate("MainWindow", "Войти"))
        self.but_install.setText(_translate("MainWindow", "Установить сборку"))
        self.but_registration.setText(_translate("MainWindow", "Зарегистрироваться"))
        self.label_3.setText(_translate("MainWindow", "         Нет аккаунта?"))
        self.label_4.setText(_translate("MainWindow", "Память"))
        self.lab_memory.setText(_translate("MainWindow", "1024"))
        self.but_exit.setText(_translate("MainWindow", "Выйти"))
        self.but_send_skin.setText(_translate("MainWindow", "Изменить скин"))
        self.but_send_cape.setText(_translate("MainWindow", "Изменить плащ"))

    def set_max_mem(self, max_mem):
        self.horizontalSlider.setMaximum(max_mem)

    def set_mem(self, mem):
        self.horizontalSlider.setValue(mem)
        self.lab_memory.setText(str(mem))

    def get_mem(self):
        return self.horizontalSlider.value()

    def edit_mem(self, mem):
        self.lab_memory.setText(str(mem))

    def get_username(self):
        return self.line_username.text()

    def get_password(self):
        return self.line_password.text()

    def log_error(self, error):
        self.line_username.clear()
        self.line_password.clear()
        self.but_play.setText(error)

    def logged(self, username):
        self.line_password.clear()
        self.line_username.clear()
        self.line_password.close()
        self.line_username.close()
        self.but_login.close()
        self.label_2.close()
        self.but_registration.close()
        self.label_3.close()
        self.but_send_cape.show()
        self.but_send_skin.show()
        self.but_exit.show()
        self.label.setText("Привет, " + username)

    def unlogged(self):
        self.line_password.show()
        self.line_username.show()
        self.but_login.show()
        self.label_2.show()
        self.but_registration.show()
        self.label_3.show()
        self.but_send_cape.close()
        self.but_send_skin.close()
        self.but_exit.close()
        self.label.setText("Имя Пользователя")

    def start_downloading(self):
        self.but_play.setEnabled(False)
        self.progressBar.show()
        self.progressBar.setValue(0)
        self.but_play.setText('Загрузка файлов')
        self.but_install.setText("Отмена")

    def end_downloading(self):
        self.but_play.setEnabled(True)
        self.but_play.setText('Играть')
        self.but_install.setText("Установить сборку")
        self.progressBar.close()

    def start_installing(self):
        self.but_play.setText("Установка")
        self.progressBar.close()

    def set_text_on_but_play(self, error):
        self.but_play.setText(error)

    def edit_progress_value(self, value):
        self.progressBar.setValue(value)