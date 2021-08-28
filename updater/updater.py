import sys
import os
import requests
import tempfile

print("Загрузка начинается")
path_to_installing = os.path.dirname(sys.executable)
OS = sys.argv[1]
url = sys.argv[2]


def downloading(path_to_installing, OS, url):
    try:
        response = requests.get(url, stream=True)
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения. Введите Y для повторной загрузки, для выхода просто нажмите 'Enter',"
              " или просто закройте консоль (подпищики Шевцова могут не догодаться).")
        answer = input()
        if answer == "Y":
            downloading(path_to_installing, OS, url)
        else:
            return
    if response.status_code == 404:
        print("Ошибка подключения. Введите Y для повторной загрузки, для выхода просто нажмите 'Enter',"
              " или просто закройте консоль (подпищики Шевцова могут не догодаться).")
        answer = input()
        if answer == "Y":
            downloading(path_to_installing, OS, url)
        else:
            return
    fp = tempfile.TemporaryFile()
    size = int(response.headers.get('Content-Length', '0'))
    downloaded_size = 0
    last_percent = 0
    for chunk in response.iter_content(chunk_size=1024*1024):
        if chunk:  # filter out keep-alive new chunks
            downloaded_size += 1024 * 1024
            if downloaded_size * 100 // size > last_percent:
                last_percent = downloaded_size * 100 // size
                if last_percent <= 100:
                    print("Лаунчер загружен на {}%".format(last_percent))
            fp.write(chunk)
    if OS == "Linux":
        launcher_path = os.path.join(path_to_installing, "Mine")
    elif OS == "Windows":
        launcher_path = os.path.join(path_to_installing, "Mine.exe")

    print("Начинается установка")
    with open(launcher_path, "wb") as f:
        f.write(fp.read())
        f.close()
    fp.close()
    print("Вiтаю! Установка новой версии лаунчера завершина.")


downloading(path_to_installing, OS, url)
