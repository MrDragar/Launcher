#!/usr/bin/python3
import os
import shutil
import sys
import requests
import time

import zipfile

url = sys.argv[1]

down = requests.get('http://' + url + '/update', stream=True)

path = sys.argv[2]
shutil.rmtree(path)
time.sleep(5)
os.mkdir(path)

with open(path+'/1.zip', 'wb') as f:
    for chunk in down.iter_content(chunk_size=1024):

        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
zfile = zipfile.ZipFile(path+'/1.zip')
zfile.extractall(path+'/')
zfile.close()
os.remove(path+'/1.zip')
