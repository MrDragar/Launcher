#!/usr/bin/python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

import minecraft_launcher_lib
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from minecraft_launcher_lib.utils import get_minecraft_directory
from psutil import virtual_memory
from PyQt5.QtWidgets import QFileDialog

from config import conf_url, conf_version, conf_launch_name, launch_dir, maincraft_version
from mainwind import Ui_MainWindow
from registration import Ui_RegWind
from updaterwind import Ui_UpdaterWindow


class downloading(QThread):
    def __init__(self, mainwindow, url, launch_name, parents=None):
        super(downloading, self).__init__(parents)
        self.mainwindow = mainwindow
        self.url = url
        self.launch_name = launch_name

    def run(self):
        down_url = 'http://' + self.url + '/modpack'
        if sys.platform == 'linux':
            OS = 'linux'
        else:
            OS = 'windows'
        data = {
            'OS': OS
        }
        try:
            response = requests.post(down_url, data=data, stream=True)
        except:
            return
        file = tempfile.TemporaryFile()
        file.write(response.content)
        fzip = zipfile.ZipFile(file)
        self.mainwindow.but_play.setEnabled(False)
        self.mainwindow.but_play.setText('Загрузка файлов')
        self.mainwindow.but_install.setEnabled(False)
        directory = get_minecraft_directory()
        directory = directory[0:(len(directory)) - 10]
        if not os.path.exists(directory + '.' + self.launch_name):
            os.mkdir(directory + '.' + self.launch_name)
        else:
            list = os.listdir(directory + '.' + self.launch_name)
            for i in list:
                if i != 'saves' and i != 'mem.json' and i != 'profile.json' and i != 'journeymap' \
                        and i != 'resourcepacks' and i != 'shaderpacks':
                    try:
                        shutil.rmtree(directory + '.' + self.launch_name + '/' + i)
                    except:
                        os.remove(directory + '.' + self.launch_name + '/' + i)

        self.mainwindow.but_play.setText('Установка файлов')
        fzip.extractall(directory + '.' + self.launch_name + '/')
        file.close()
        fzip.close()
        self.mainwindow.but_play.setEnabled(True)
        self.mainwindow.but_play.setText('Играть')
        self.mainwindow.but_install.setEnabled(True)


class MyLauncher:
    def __init__(self):
        # Вычисление максимально возможного количества оперативной памяти
        self.maxmem = (virtual_memory().total // 1024 // 4 // 1024 * 3)

        # Получаем путь до места, где будет лежать папка с клиентом
        if sys.platform == "linux" or "linux2":
            self.directory = os.path.join(os.path.join(os.environ['HOME']), 'calendar')
        else:
            self.directory = os.path.join(os.path.join(os.environ['HOME']), 'calendar')
        # self.directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        # self.directory = self.directory[0:(len(self.directory)) - 10]
        self.launch_dir = launch_dir
        # Запускаем приложение
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        # Информация о лаунчере и url до сайта
        self.url = conf_url
        self.__version__ = conf_version
        self.launch_name = conf_launch_name
        self.load_mem()
        self.load_user()

        # Создаём оюъект для установки сборки
        self.ui.down = downloading(mainwindow=self.ui, url=self.url, launch_name=self.launch_name)

        #  Настройки подключения кнопок
        self.ui.horizontalSlider.valueChanged.connect(self.edit_mem)
        self.ui.but_registration.clicked.connect(self.openReg)
        self.ui.but_install.clicked.connect(self.ui.down.start)
        self.ui.but_login.clicked.connect(self.login)
        self.ui.but_exit.clicked.connect(self.exit)
        self.ui.but_play.clicked.connect(self.play)
        self.ui.but_send_skin.clicked.connect(self.send_skin)
        self.ui.but_send_cape.clicked.connect(self.send_cape)
        self.ui.but_login.setShortcut('Return')

        if sys.platform != 'linux':
            self.update()

        sys.exit(self.app.exec_())

    def load_user(self):
        try:

            with open(self.directory + '.' + self.launch_name + '/' + "profile.json", 'r', encoding='utf-8') as f:
                self.sett = json.load(f)
            if self.sett['username'] != '' and self.sett['UUID'] != '' and self.sett['Token'] != '':
                self.ui.line_password.close()
                self.ui.line_email.close()
                self.ui.but_login.close()
                self.ui.label_2.close()
                self. ui.but_registration.close()
                self.ui.label_3.close()
                self.ui.but_exit.show()
                self.ui.label.setText('Привет,  ' + self.sett['username'])
                self.ui.but_send_cape.show()
                self.ui.but_send_skin.show()
            else:
                self. ui.line_password.show()
                self.ui.line_email.show()
                self. ui.but_login.show()
                self. ui.label_2.show()
                self. ui.but_registration.show()
                self. ui.label_3.show()
                self. ui.but_exit.close()
                self. ui.label.setText('Имя пользователя')
                self. ui.but_send_cape.close()
                self.  ui.but_send_skin.close()
        except:
            pass

    def load_mem(self):
        try:
            with open(self.directory + '.' + self.launch_name + '/' + "mem.json", 'r',
                      encoding='utf-8') as f:  # открыли файл с данными
                dict_mem = json.load(f)  # загнали все, что получилось в переменную
                self.mem = int(dict_mem['mem'])
        except:
            # При неудаче создаём файл mem.json и ставим по дефолту 1024 Мб
            if not os.path.exists(self.directory + '.' + self.launch_name + '/'):
                os.mkdir(self.directory + '.' + self.launch_name + '/')
            dict_mem = {
                'mem': '1024',
            }
            self.mem = 1024
            with open(self.directory + '.' + self.launch_name + '/' + "mem.json", 'w') as f:
                json.dump(dict_mem, f)

        # Выводим значение памяти на интерфейс и изменяем ползунок памяти
        self.ui.horizontalSlider.setMaximum(self.maxmem)
        self.ui.lab_memory.setText(str(dict_mem['mem']))
        self.ui.horizontalSlider.setValue(int(dict_mem['mem']))

    def edit_mem(self):
        self.mem = self.ui.horizontalSlider.value()
        if not os.path.exists(self.directory + '.' + self.launch_name + '/'):
            os.mkdir(self.directory + '.' + self.launch_name + '/')
        setmem = {
            'mem': self.mem,
        }
        with open(self.directory + '.' + self.launch_name + '/' + "mem.json", 'w') as f:
            json.dump(setmem, f)
        self.ui.lab_memory.setText(str(self.mem))

    def send_cape(self):
        path = QFileDialog.getOpenFileName()[0]
        try:
            f = open(path, 'rb')
            username = self.sett['username']
            response = requests.post('http://' + conf_url + '/texture', files={'cape/' + username + '.png': f})
            if response.content == b'':
                self.ui.but_send_cape.setText('Плащ успешно загружен')
            else:
                self.ui.but_send_cape.setText('Произошла ошибка')
        except:
            self.ui.but_send_cape.setText('Произошла ошибка')

    def send_skin(self):
        path = QFileDialog.getOpenFileName()[0]
        try:
            f = open(path, 'rb')
            username = self.sett['username']
            response = requests.post('http://' + conf_url + '/texture', files={'skin/' + username + '.png': f})
            if response.content == b'':
                self.ui.but_send_skin.setText('Скин успешно загружен')
            else:
                self.ui.but_send_skin.setText('Произошла ошибка')
        except:
            self.ui.but_send_skin.setText('Произошла ошибка')

    def login(self):
        name = self.ui.line_email.text()
        login = self.ui.line_password.text()
        payload = {

            "username": name,
            "password": login,
        }
        try:
            response = requests.post('http://' + self.url + '/login', data=payload)
        except:
            return
        a = json.loads(response.content)
        if a['status'] == 'ERROR':
            self.ui.line_password.clear()
            self.ui.line_email.clear()
        elif a['status'] == 'OK':
            self.ui.line_password.close()
            self.ui.line_email.close()
            self.ui.but_login.close()
            self.ui.label_2.close()
            self.ui.but_registration.close()
            self.ui.label_3.close()
            self.ui.line_password.clear()
            self.ui.line_email.clear()
            self.ui.but_send_cape.show()
            self.ui.but_send_skin.show()
            b = a['message'].split(':')
            self.sett = {
                "username": b[0],
                "UUID": b[1],
                "Token": b[2]
            }
            if not os.path.exists(self.directory + '.' + self.launch_name + '/'):
                os.mkdir(self.directory + '.' + self.launch_name + '/')
            with open(self.directory + '.' + self.launch_name + '/' + "profile.json", 'w') as f:
                json.dump(self.sett, f)
            self.ui.label.setText('Привет,  ' + b[0])
            self.ui.but_exit.show()

    def exit(self):
        self.ui.line_password.show()
        self.ui.line_email.show()
        self.ui.but_login.show()
        self.ui.label_2.show()
        self.ui.but_registration.show()
        self.ui.label_3.show()
        self.ui.but_exit.close()
        os.remove(self.directory + '.' + self.launch_name + '/' + "profile.json")
        self.ui.label.setText("Имя пользователя")
        self.ui.but_send_cape.close()
        self.ui.but_send_skin.close()
        self.sett = {
            "username": '',
            "UUID": '',
            "Token": ''
        }

    def play(self):
        try:
            self.MainWindow.close()
            options = {
                "username": self.sett['username'],
                "uuid": self.sett['UUID'],
                "token": self.sett['Token'],
                "jvmArguments": ['-Xmx' + str(self.mem) + 'M']
            }
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(maincraft_version,
                                                                                     self.directory + '.' +
                                                                                     self.launch_name + '/',
                                                                                     options)

            subprocess.call(minecraft_command)
        except:
            self.MainWindow.show()
            self.ui.but_play.setText('Переустановите сборку или войдите в аккаунт')

    def openReg(self):
        RegWind = QtWidgets.QMainWindow()
        ui = Ui_RegWind()
        ui.setupUi(RegWind)
        RegWind.show()
        self.MainWindow.close()
        ui.but1_send.setShortcut('Return')

        def returnToMain():
            self.MainWindow.show()
            RegWind.close()

        def send():
            new_name = ui.line1_name.text()
            pasw1 = ui.line1_password1.text()
            pasw2 = ui.line1_password1_2.text()
            mail = ui.line1_email.text()
            payload = {
                "username": new_name,
                "password1": pasw1,
                "password2": pasw2,
                "email": mail
            }
            try:
                response = requests.post('http://' + self.url + '/registration', data=payload)
            except:
                return
            e = json.loads(response.content)
            if e['status'] == "ERROR":
                ui.line1_email.clear()
                ui.label_error.setText(e['message'])
                ui.label_error.show()
                ui.line1_name.clear()
                ui.line1_password1.clear()
                ui.line1_password1_2.clear()
            else:
                ui.label_error.close()
                returnToMain()

        ui.but1_cancel.clicked.connect(returnToMain)
        ui.but1_send.clicked.connect(send)

    def update(self):
        try:
            response = requests.get('http://' + self.url + '/version')
        except:
            return
        new_version = json.loads(response.content)
        number = new_version['number']

        if self.__version__ != number:
            UpdWind = QtWidgets.QMainWindow()
            ui2 = Ui_UpdaterWindow()
            ui2.setupUi(UpdWind)
            UpdWind.show()
            self.MainWindow.close()

            def No():
                self.MainWindow.show()
                UpdWind.close()

            def Yes():
                UpdWind.close()
                upt_dir = self.directory + self.launch_dir + '/Updater/dist/updater/updater.exe'
                launch_dir_def = self.directory + self.launch_dir + '/Launcher'
                subprocess.Popen([upt_dir, self.url, launch_dir_def])
                sys.exit()

            ui2.pushButton_2.clicked.connect(No)
            ui2.pushButton.clicked.connect(Yes)


MyApp = MyLauncher()
