import os
import re

import pytube
import requests
from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("videoDownloader.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def download_video():
    global data_id

    if yt_streams is not None and len(data_id) == 1:
        yt_streams.get_by_itag(*data_id).download(output_path=form.lineEdit_2.text())


def choose_path():
    file_path = QtWidgets.QFileDialog.getExistingDirectory()
    form.lineEdit_2.setText(file_path)


def change_audio():
    global videoData, currentSettings

    currentSettings = {
        "res": None,
        "fps": None,
        "ext": None,
        "wa": form.checkBox.isChecked()
    }

    put_data_to_combobox(videoData, form.checkBox.isChecked())


def check_link():
    pattern = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+'
    url = form.lineEdit.text()

    if re.match(pattern, url) is not None:
        try:
            response = requests.get(url)
            print(response)
            is_youtube_link = 200 <= response.status_code < 300 and pytube.extract.playability_status(
                pytube.YouTube(url).watch_html)
        except:
            is_youtube_link = False
    else:
        is_youtube_link = False

    if is_youtube_link:
        get_video_data()


def get_video_data():
    global videoData, yt_streams, currentSettings

    currentSettings = {
        "res": None,
        "fps": None,
        "ext": None,
        "wa": form.checkBox.isChecked()
    }

    url = form.lineEdit.text()
    yt = pytube.YouTube(url)

    yt_streams = yt.streams.filter(type="video")

    for stream in yt_streams:
        stream_id = stream.itag
        res = stream.resolution
        fps = stream.fps
        ext = stream.mime_type.split('/')[1]
        prog = stream.is_progressive
        videoData[stream_id] = {
            "res": res,
            "fps": fps,
            "ext": ext,
            "wa": prog
        }

    put_data_to_combobox(videoData, form.checkBox.isChecked())


def put_data_to_combobox(video_data, isProg):
    all_ext = get_all(video_data, "ext", isProg)
    all_ext.sort()

    all_res = get_all(video_data, "res", isProg)
    all_res = sorted([int(i[:-1]) for i in all_res])[::-1]
    all_res = [str(i) + 'p' for i in all_res]

    all_fps = get_all(video_data, "fps", isProg)
    all_fps = sorted([int(i) for i in all_fps])[::-1]
    all_fps = [str(i) for i in all_fps]

    input_data_in_combo(all_ext, form.comboBox_2, 'ext')
    input_data_in_combo(all_res, form.comboBox, 'res')
    input_data_in_combo(all_fps, form.comboBox_3, 'fps')


def input_data_in_combo(data, combobox, filterX):
    combobox.clear()
    combobox.addItem("Select...")
    combobox.addItems(data)

    if combobox.count() == 2:
        combobox.setCurrentIndex(1)
        currentSettings[filterX] = combobox.currentText()


def get_all(video_data, search_filter, is_progress):
    arr = set()

    for video in video_data:
        if video_data[video]["wa"] == is_progress:
            arr.add(str(video_data[video][search_filter]))

    return list(arr)


def filter_cb(combobox, filterCB):
    global currentSettings

    if combobox.currentIndex() != 0:
        currentSettings[filterCB] = combobox.currentText()
    else:
        currentSettings[filterCB] = None

    update_info()


def update_info():
    global data_id
    data_id = []

    t = yt_streams.filter(res=currentSettings['res'], file_extension=currentSettings['ext'],
                          adaptive=not currentSettings["wa"])
    for i in t:
        if str(i.fps) == currentSettings['fps'] or currentSettings['fps'] is None:
            data_id.append(i.itag)

    data = {k: v for k, v in videoData.items() if k in data_id}

    put_data_to_combobox(data, form.checkBox.isChecked())


videoData = {}
currentSettings = {}
yt_streams = None
data_id = []

form.pushButton.clicked.connect(choose_path)
form.lineEdit_2.setText(os.getcwd())
form.lineEdit.textChanged.connect(check_link)
form.checkBox.toggled.connect(change_audio)

form.comboBox.activated.connect(lambda: filter_cb(form.comboBox, 'res'))
form.comboBox_2.activated.connect(lambda: filter_cb(form.comboBox_2, 'ext'))
form.comboBox_3.activated.connect(lambda: filter_cb(form.comboBox_3, 'fps'))

form.pushButton_2.clicked.connect(download_video)

app.exec()
