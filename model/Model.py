import subprocess
from PyQt5.QtCore import QThread
import requests
import sys
import tempfile
import shutil
import os
import zipfile
import minecraft_launcher_lib
from psutil import virtual_memory
from config.config import url, launcher_version, client_dir, launch_dir, maincraft_version
import json


class Model:
    def __init__(self):

        if not ("http://" or "https://") in url:
            self.url = 'http://' + url
        else:
            self.url = url

        if getattr(sys, 'frozen', False):
            self.launcher_path = sys.executable
            self.launcher_dir = os.path.dirname(sys.executable)
            self.frozen = False
        else:
            self.launcher_dir = os.path.dirname(os.path.abspath(__file__))
            self.launcher_path = os.path.abspath(__file__)
            self.frozen = True

        if sys.platform == "linux" or "linux2":
            self.client_directory = os.environ['HOME']
            self.updater_path = os.path.join(self.launcher_dir, "updater")
            self.OS = "Linux"
            self.update_url = self.url + "/static/Mine/zip/main"

        else:
            self.client_directory = os.environ['APPDATA']
            self.updater_path = os.path.join(self.launcher_dir, "updater.exe")
            self.OS = "Windows"
            self.update_url = self.url + "/static/Mine/zip/main.exe"
        self.client_directory = os.path.join(self.client_directory, client_dir)

        self.login_url = self.url + '/login'
        self.registration_url = self.url + "/registration"
        self.version_url = self.url + "/version"
        self.launcher_version = launcher_version

    @property
    def load_mem(self):
        if os.path.exists(os.path.join(self.client_directory, "mem.json")):
            with open(os.path.join(self.client_directory, "mem.json"), 'r') as f:
                dict_mem = json.load(f)
                if dict_mem.__class__ is dict:
                    if 'mem' in dict_mem:
                        if dict_mem["mem"].__class__ is int:
                            self.mem = dict_mem["mem"]
                            return self.mem
        if not os.path.exists(self.client_directory):
            os.mkdir(self.client_directory)
        with open(os.path.join(self.client_directory, "mem.json"), 'w') as f:
            self.mem = 1024
            json.dump({"mem": 1024}, f)
        return self.mem

    @staticmethod
    def max_mem():
        return virtual_memory().total // 1024 // 4 // 1024 * 3

    def edit_mem(self, mem):
        self.mem = mem
        if os.path.exists(os.path.join(self.client_directory, "mem.json")):
            with open(os.path.join(self.client_directory, "mem.json"), 'w') as f:
                json.dump({"mem": mem}, f)

    def login(self, username, password):
        try:
            page = requests.get(self.login_url)
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": "lost connection"}
        data = {"username": username,
                "password": password
                }
        response = requests.post(self.login_url, data=data)
        if response.status_code == 404:
            return {"status": "error", "message": "lost connection"}
        content = json.loads(response.content)
        if content["status"] == "OK":
            username = content["message"]["username"]
            uuid = content["message"]["uuid"]
            accessToken = content["message"]["accessToken"]
            params = {
                "username": username,
                "uuid": uuid,
                "accessToken": accessToken,
            }
            if not os.path.exists(self.client_directory):
                os.mkdir(self.client_directory)
            with open(os.path.join(self.client_directory, "profile.json"), "w") as f:
                json.dump(params, f)
            return {"status": "OK", "username": username}
        else:
            return content

    def registration(self, data):
        try:
            page = requests.get(self.registration_url)
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": "lost connection"}
        response = requests.post(self.registration_url, data=data)
        if response.status_code == 404:
            return {"status": "error", "message": "lost connection"}
        content = json.loads(response.content)
        return content

    def exit(self):
        if not os.path.exists(self.client_directory):
            os.mkdir(self.client_directory)
        with open(os.path.join(self.client_directory, "profile.json"), "w") as f:
            json.dump({}, f)

    def check_auth(self):
        if not os.path.exists(os.path.join(self.client_directory, "profile.json")):
            return False, None
        else:
            with open(os.path.join(self.client_directory, "profile.json"), "r") as f:
                content = f.read()
                if content != '':
                    data = json.loads(content)
                    if data.__class__ is dict:
                        if "username" and "uuid" and "accessToken" in data:
                            if data["username"] and data["uuid"] and data["accessToken"] != '':
                                return True, data["username"]
        return False, None

    def play(self, mem):
        with open(os.path.join(self.client_directory, "profile.json"), "r") as f:
            content = f.read()
            if content != '':
                data = json.loads(content)
                if data.__class__ is dict:
                    if "username" and "uuid" and "accessToken" in data:
                        if data["username"] and data["uuid"] and data["accessToken"] != '':
                            try:
                                options = {
                                    "username": data['username'],
                                    "uuid": data['uuid'],
                                    "token": data['accessToken'],
                                    "jvmArguments": ['-Xmx' + str(mem) + 'M']
                                }
                                minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
                                    maincraft_version,
                                    self.client_directory,
                                    options)

                            except:
                                return "Error_of_run"
                            subprocess.Popen(minecraft_command)
                            sys.exit()
                        else:
                            return "Вы не авторизовались"
                    else:
                        return "Вы не авторизовались"
                else:
                    return "Вы не авторизовались"
            else:
                return "Вы не авторизовались"

    def check_new_version(self):
        if self.frozen:
            return False
        try:
            page = requests.get(self.version_url, timeout=1)
        except requests.exceptions.ConnectionError:
            return False
        response = requests.get(self.version_url)
        if response.status_code == 404:
            return False
        if json.loads(response.content)["number"] == self.launcher_version:
            return False
        else:
            return True

    def start_update(self):
        try:
            subprocess.Popen([self.updater_path, self.OS, self.update_url])
            sys.exit()
        except:
            pass


class Modal_downloading(QThread):
    def __init__(self, end_downloading, start_installing, progress_bar, check_cancel, parents=None):
        super(Modal_downloading, self).__init__(parents)
        self.check_cancel = check_cancel
        self.end_downloading = end_downloading
        self.progress_bar = progress_bar
        self.start_installing = start_installing
        self.url = url
        if sys.platform == "linux" or sys.platform ==  "linux2":
            self.client_directory = os.environ['HOME']
        else:
            self.client_directory = os.environ['APPDATA']
        self.client_directory = os.path.join(self.client_directory, client_dir)

    def run(self):
        down_url = 'http://' + self.url + '/static/Mine/zip/MyModPack.zip'
        try:
            response = requests.get(down_url, stream=True)
        except requests.exceptions.ConnectionError:
            return self.end_downloading()
        if response.status_code == 404:
            return self.end_downloading()
        file = tempfile.TemporaryFile()
        size = int(response.headers.get('Content-Length', '0'))
        downloaded_size = 0
        last_percent = 0
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:  # filter out keep-alive new chunks
                downloaded_size += 1024*1024
                if not self.check_cancel():
                    if downloaded_size * 100 // size > last_percent:
                        last_percent = downloaded_size * 100 // size
                        if last_percent <= 100:
                            self.progress_bar(last_percent)
                    file.write(chunk)
                else:
                    self.end_downloading()
        fzip = zipfile.ZipFile(file)
        self.start_installing()
        if not os.path.exists(self.client_directory):
            os.mkdir(self.client_directory)
        else:
            list = os.listdir(self.client_directory)
            for i in list:
                if i != 'saves' and i != 'mem.json' and i != 'profile.json' and i != 'journeymap' \
                        and i != 'resourcepacks' and i != 'shaderpacks':
                    if os.path.isdir(os.path.join(self.client_directory, i)):
                        shutil.rmtree(os.path.join(self.client_directory, i))
                    else:
                        os.remove(os.path.join(self.client_directory, i))
        fzip.extractall(self.client_directory)

        file.close()
        fzip.close()
        self.end_downloading()
