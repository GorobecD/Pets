from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore
import random

Form, Window = uic.loadUiType("targetpractice.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

startBT = form.pushButton_2
targetBT = form.pushButton
scoreLB = form.label_3
timeLB = form.label

targetBT.hide()
scoreLB.setText('0')
timeLB.setText('00:00')


class Thread(QtCore.QThread):
    def stop(self):
        self._stopped = True
        print("STOPPING LOOP")

    def run(self):
        self._stopped = False
        print("STARTING LOOP")


class TimeThread(Thread):
    def run(self):
        self._stopped = False
        counter = 0
        while not self._stopped:
            self.msleep(1000)
            counter += 1
            update_timer(counter)


class DespawnThread(Thread):

    def run(self):
        self._stopped = False
        self.despawn_time = 1
        self.score = int(scoreLB.text())
        self.time = 0

        while not self._stopped:
            self.score = int(scoreLB.text())

            self.msleep(200)
            self.time += 0.2

            if self.time >= self.despawn_time:
                self.time = 0
                create_target()

    def setTime(self, secs):
        self.time = secs


def update_timer(secs):
    minutes = str(secs // 60)
    seconds = str(secs % 60)

    if len(minutes) == 1:
        minutes = "0" + minutes

    if len(seconds) == 1:
        seconds = "0" + seconds

    timeLB.setText(f"{minutes}:{seconds}")


def hit_target():
    scoreLB.setText(str(int(scoreLB.text()) + 1))
    despawnThread.setTime(0)

    create_target()

    if not despawnThread.isRunning():
        despawnThread.start()


def create_target():
    x, y = generate_coordinates()
    spawn_target(x, y)


def generate_coordinates():
    global targetRadius

    return random.randint(targetRadius, window.width() - targetRadius), \
        random.randint(10 + targetRadius, window.height() - targetRadius-76)


def spawn_target(x, y):
    targetBT.move(x, y)


def start_game():
    startBT.hide()
    targetBT.show()
    timeThread.start()


targetRadius = 38
form.pushButton_2.clicked.connect(start_game)
targetBT.clicked.connect(hit_target)

timeThread = TimeThread()
despawnThread = DespawnThread()
app.exec()
