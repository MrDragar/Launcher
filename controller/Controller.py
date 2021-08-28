from model.Model import Model, Modal_downloading
from view.View import Ui_MainWindow
from view.registration_window import Ui_RegWind
from view.updaterwind import Ui_UpdaterWindow
from PyQt5 import QtWidgets
from PyQt5 import Qt


class Controller(Qt.QApplication):
    def __init__(self, sys_argv):
        """Создаём само приложение"""
        super(Controller, self).__init__(sys_argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(self.MainWindow)
        self.ui_reg = Ui_RegWind(self.MainWindow)
        self.ui_updater = Ui_UpdaterWindow(self.MainWindow)
        self.model = Model()
        self.modal_downloading = Modal_downloading(self.end_downloading, self.start_installing, self.edit_progress_bar,
                                                   self.check_cancel)
        self.start_program()
        self.installing = False
        self.cancel_download = False

    def open_main_window(self):
        """открываем главное окно и настраиваем его"""
        self.ui.setup_main_window()
        self.MainWindow.show()
        self.set_max_mem()
        self.set_mem()
        self.check_auth()

        """Привязываем функции к кнопкам и горячие клавиши"""
        self.ui.but_registration.clicked.connect(self.open_registration_window)
        self.ui.horizontalSlider.valueChanged.connect(self.edit_mem)
        self.ui.but_install.clicked.connect(self.download)
        self.ui.but_login.clicked.connect(self.login)
        self.ui.but_exit.clicked.connect(self.exit)
        self.ui.but_play.clicked.connect(self.play)
        # self.ui.but_send_skin.clicked.connect(self.model.send_skin)
        # self.ui.but_send_cape.clicked.connect(self.model.send_cape)

        self.ui.but_login.setShortcut('Return')

    def open_registration_window(self):
        """открываем окно регистрации и настраиваем в нём кнопки"""
        self.ui_reg.setup_registration_window()
        self.MainWindow.show()
        self.ui_reg.but1_cancel.clicked.connect(self.open_main_window)
        self.ui_reg.but1_send.clicked.connect(self.registration)

    def open_updater_window(self):
        """открываем окно обновления и настраиваем в нём кнопки"""
        self.ui_updater.setupUi()
        self.MainWindow.show()
        self.ui_updater.pushButton_2.clicked.connect(self.open_main_window)
        self.ui_updater.pushButton.clicked.connect(self.start_update)

    def set_max_mem(self):
        """Выставляем верхнюю границу ползунка памяти"""
        self.ui.set_max_mem(self.model.max_mem())

    def set_mem(self):
        """Выставляем значение памяти"""
        self.ui.set_mem(self.model.load_mem)

    def edit_mem(self):
        """Изменяем количество памяти, веделенное на запкск minecraft"""
        mem = self.ui.get_mem()
        self.model.edit_mem(mem)
        self.ui.edit_mem(mem)

    def login(self):
        """Логинимся на сайте"""
        username = self.ui.get_username()
        password = self.ui.get_password()
        data = self.model.login(username=username, password=password)
        if data["status"] == "OK":
            self.ui.logged(data["username"])
        else:
            self.ui.log_error(data["message"])

    def exit(self):
        self.ui.unlogged()
        self.model.exit()

    def check_auth(self):
        auth, username = self.model.check_auth()
        if auth:
            self.ui.logged(username)
        else:
            self.ui.unlogged()
        pass

    def download(self):
        if not self.installing:
            self.modal_downloading.start()
            self.ui.start_downloading()
            self.installing = True
            self.cancel_download = False
        else:
            self.cancel_download = True

    def check_cancel(self):
        return self.cancel_download

    def edit_progress_bar(self, value):
        self.ui.edit_progress_value(value)

    def end_downloading(self):
        self.ui.end_downloading()
        self.installing = False
        self.cancel_download = False

    def start_installing(self):
        self.ui.start_installing()

    def play(self):
        self.MainWindow.close()
        mem = self.ui.get_mem()
        error = self.model.play(mem)
        self.MainWindow.show()
        if error == None:
            error = 'Играть'
        self.ui.set_text_on_but_play(error)

    def registration(self):
        data = self.ui_reg.get_data_for_registration()
        content = self.model.registration(data)
        if content["status"] == "OK":
            self.open_main_window()
            self.ui.set_text_on_but_play("Подтвердите свою почту")
        else:
            self.ui_reg.registration_error(content["message"])
        pass

    def start_program(self):
        new_update = self.model.check_new_version()
        if new_update:
            self.open_updater_window()
        else:
            self.open_main_window()

    def start_update(self):
        self.MainWindow.close()
        self.model.start_update()
