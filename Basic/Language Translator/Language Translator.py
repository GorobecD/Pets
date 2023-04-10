from deep_translator import GoogleTranslator
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("translator.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


class Thread(QtCore.QThread):
    finished = pyqtSignal()

    def stop(self):
        self._stopped = True

    def run(self):
        self._stopped = False
        self.wait_time = 0.5
        self.time = 0
        while not self._stopped and self.wait_time >= self.time:
            self.msleep(250)
            self.time += 0.25

        self.result = translate()
        self.finished.emit()

    def reset_time(self):
        self.time = 0


def swap_translations():
    if textLanguageCB.currentIndex() != 0:
        textIN, textOUT = inputTextTE.toPlainText(), outputTextTE.toPlainText()
        inputTextTE.setText(textOUT)
        outputTextTE.setText(textIN)

        languageIN, languageOUT = textLanguageCB.currentText(), translateLanguageCB.currentText()
        index1 = textLanguageCB.findText(languageOUT)
        index2 = translateLanguageCB.findText(languageIN)
        textLanguageCB.setCurrentIndex(index1)
        translateLanguageCB.setCurrentIndex(index2)

        on_edit_translate()


def translate():
    if textLanguageCB.currentIndex() == 0:
        source_tl = "auto"
    else:
        source_tl = textLanguageCB.currentText().lower()

    target_tl = translateLanguageCB.currentText().lower()

    return GoogleTranslator(source=source_tl, target=target_tl).translate(text=inputTextTE.toPlainText())


def on_edit_translate():
    global trans, thread

    if thread.isRunning():
        thread.reset_time()
    else:
        thread.start()

    thread.finished.connect(lambda: outputTextTE.setText(thread.result))


thread = Thread()
trans = ''
swapBT = form.pushButton
textLanguageCB = form.comboBox
translateLanguageCB = form.comboBox_2
inputTextTE = form.textEdit
outputTextTE = form.textEdit_2

translationLanguages = list(map(lambda x: x.capitalize(), GoogleTranslator().get_supported_languages()))
textLanguages = ["Detect language"] + translationLanguages

textLanguageCB.addItems(textLanguages)
translateLanguageCB.addItems(translationLanguages)

swapBT.clicked.connect(swap_translations)
inputTextTE.textChanged.connect(on_edit_translate)
textLanguageCB.activated.connect(on_edit_translate)
translateLanguageCB.activated.connect(on_edit_translate)

app.exec()
