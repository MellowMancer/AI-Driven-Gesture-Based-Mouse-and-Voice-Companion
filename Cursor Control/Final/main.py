import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from voice_main import call_for_voice
from hand_main import call_for_gesture
import multiprocessing
import os

class WorkerThread(QThread):
    finished = pyqtSignal()

    def run(self):
        # Simulate a long-running task
        self.sleep(5)
        self.finished.emit()

class ManualWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual")
        self.setGeometry(200, 200, 800, 460)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), 'manual.png')))
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, 800, 460)

    def open_image(self, path):
        self.label.setPixmap(QPixmap(path))
        label = QLabel()
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        self.setWindowTitle("Manual")
        self.show()

class MainWindow(QMainWindow):

    def handFontColor(self) -> None:
        self.hand_status *= -1
        if self.hand_status == 1:
            self.button1.setStyleSheet(f'QPushButton {{ background-color: #262529; color: grey; font: bold 30px; }}')
            self.button3.setStyleSheet(f'QPushButton {{ background-color: #262529; color: white; font: bold 25px; }}' 
                                       f'QPushButton:hover {{ background-color: #262529; color: #f02e61; font: bold 28px;}}')
        else:
            self.button1.setStyleSheet(f'QPushButton {{ background-color: #262529; color: white; font: bold 30px; }}'
                                    f'QPushButton:hover {{ background-color: #262529; color: #f02e61; font: bold 35px;}}')
            self.button3.setStyleSheet(f'QPushButton {{ background-color: #262529; color: grey; font: bold 25px; }}')

    def voiceFontColor(self) -> None:
        self.voice_status *= -1
        if self.voice_status == 1:
            self.button2.setStyleSheet(f'QPushButton {{ background-color: #262529; color: grey; font: bold 30px; }}')
            self.button4.setStyleSheet(f'QPushButton {{ background-color: #262529; color: white; font: bold 25px; }}' 
                                       f'QPushButton:hover {{ background-color: #262529; color: #f02e61; font: bold 28px;}}')
        else:
            self.button2.setStyleSheet(f'QPushButton {{ background-color: #262529; color: white; font: bold 30px; }}'
                                    f'QPushButton:hover {{ background-color: #262529; color: #f02e61; font: bold 35px;}}')
            self.button4.setStyleSheet(f'QPushButton {{ background-color: #262529; color: grey; font: bold 25px; }}')

    def update_loading1(self):
        self.load1 *= -1
        if self.load1 == 1:
            self.loading1.setStyleSheet(f'QLabel {{ background-color: rgba(0,0,0,0); color: grey; font: bold 20px; }}')
        else:
            self.loading1.setStyleSheet(f'QLabel {{ background-color: rgba(0,0,0,0); color: #262529; font: bold 20px; }}')    

    def update_loading2(self):
        self.load2 *= -1
        if self.load2 == 1:
            self.loading2.setStyleSheet(f'QLabel {{ background-color: rgba(0,0,0,0); color: grey; font: bold 20px; }}')
        else:
            self.loading2.setStyleSheet(f'QLabel {{ background-color: rgba(0,0,0,0); color: #262529; font: bold 20px; }}')

    def start_hand_detection(self):
        if not hasattr(self, 'hand_process'):
            self.hand_process = multiprocessing.Process(target=call_for_gesture, args=(self.hand_terminate_queue,))
            # self.update_loading1()
            self.handFontColor()
            self.hand_process.start()

    def stop_hand_detection(self):
        if hasattr(self, 'hand_process'):
            self.handFontColor()
            self.hand_terminate_queue.put("terminate")
            # self.hand_process.terminate()
            # self.hand_process.join()

    def start_speech_detection(self):
        if not hasattr(self, 'voice_process'):
            self.voice_process = multiprocessing.Process(target=call_for_voice, args=(self.voice_terminate_queue,))
            # self.update_loading2()
            self.voiceFontColor()
            self.voice_process.start()

    def stop_speech_detection(self):
        if hasattr(self, 'voice_process'):
            self.voiceFontColor()
            self.voice_terminate_queue.put("terminate")
            # self.voice_process.terminate()
            # self.voice_process.join()

    def open_manual(self, checked):
        self.new = ManualWindow()
        self.new.show()
        # manual_window = QWidget()
        # label = QLabel(manual_window)
        # pixmap = QPixmap("./manual.png")
        # label.setPixmap(pixmap)
        # label.setScaledContents(True)
        # manual_window.setWindowTitle("Manual Window")
        # print("Hola")
        # manual_window.show()


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Waver")
        self.setGeometry(200, 200, 800, 460)

        self.hand_terminate_queue = multiprocessing.Queue()
        self.voice_terminate_queue = multiprocessing.Queue()
        self.load1 = -1
        self.load2 = -1
        self.hand_status = -1
        self.voice_status = -1

        self.button0 = QPushButton("Manual", self)
        self.button0.setGeometry(0, 0, 800, 60)
        self.button0.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 25px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 28px;}")
        self.button0.clicked.connect(self.open_manual)

        self.button1 = QPushButton("Start Hand Detection", self)
        self.button1.setGeometry(0, 60, 400, 340)
        self.button1.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px; }"
                                   "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
        self.button1.clicked.connect(self.start_hand_detection)

        self.loading1 = QLabel("Loading...", self)
        self.loading1.setGeometry(100, 260, 100, 140)
        self.loading1.setStyleSheet("QLabel { background-color: rgba(0,0,0,0); color: #262529; font: bold 20px; }")

        self.button2 = QPushButton("Start Voice Detection", self)
        self.button2.setGeometry(400, 60, 400, 340)
        self.button2.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
        self.button2.clicked.connect(self.start_speech_detection)

        self.loading2 = QLabel("Loading...", self)
        self.loading2.setGeometry(500, 260, 100, 140)
        self.loading2.setStyleSheet("QLabel { background-color: rgba(0,0,0,0); color: #262529; font: bold 20px; }")

        self.button3 = QPushButton("Stop Hand Detection", self)
        self.button3.setGeometry(0, 400, 400, 60)
        self.button3.setStyleSheet("QPushButton { background-color: #262529; color: grey; font: bold 25px; }")
        self.button3.clicked.connect(self.stop_hand_detection)

        self.button4 = QPushButton("Stop Voice Detection", self)
        self.button4.setGeometry(400, 400, 400, 60)
        self.button4.setStyleSheet("QPushButton { background-color: #262529; color: grey; font: bold 25px; }")
        self.button4.clicked.connect(self.stop_speech_detection)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()