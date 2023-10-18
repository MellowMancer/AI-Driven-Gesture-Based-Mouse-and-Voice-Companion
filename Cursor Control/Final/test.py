import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from voice_main import call_for_voice
from hand_main import call_for_gesture
import multiprocessing
import os

class MainWindow(QMainWindow):

    def start_hand_detection(self):
        self.hand_process = multiprocessing.Process(target=call_for_gesture)
        self.hand_process.start()

    def stop_hand_detection(self):
        if hasattr(self, 'hand_process'):
            self.hand_process.terminate()
            self.hand_process.join()

    def start_speech_detection(self):
        self.voice_process = multiprocessing.Process(target=call_for_voice)
        self.voice_process.start()

    def stop_speech_detection(self):
        if hasattr(self, 'voice_process'):
            self.voice_process.terminate()
            self.voice_process.join()

    def open_manual(self):
        manual_window = QMainWindow()
        manual_window.setWindowTitle("Manual")
        manual_window.setGeometry(300, 300, 800, 600)

        label = QLabel(manual_window)
        file_path = os.path.abspath("manual.pdf")
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)

        manual_window.show()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Waver")
        self.setGeometry(200, 200, 800, 460)

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

        self.button2 = QPushButton("Start Voice Detection", self)
        self.button2.setGeometry(400, 60, 400, 340)
        self.button2.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
        self.button2.clicked.connect(self.start_speech_detection)

        self.button3 = QPushButton("Stop Hand Detection", self)
        self.button3.setGeometry(0, 400, 400, 60)
        self.button3.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 25px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 28px;}")
        self.button3.clicked.connect(self.stop_hand_detection)

        self.button4 = QPushButton("Stop Voice Detection", self)
        self.button4.setGeometry(400, 400, 400, 60)
        self.button4.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 25px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 28px;}")
        self.button4.clicked.connect(self.stop_speech_detection)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())






# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PyQt6.QtGui import QFont, QColor, QPainter, QRegion
# from PyQt6.QtCore import Qt, QRectF
# from voice_main import call_for_voice
# from hand_main import call_for_gesture
# import multiprocessing

# class MainWindow(QMainWindow):

#     def start_hand_detection(self):
#         self.pool.apply_async(call_for_gesture)  # Run function1 asynchronously

#     def start_speech_detection(self):
#         self.pool.apply_async(call_for_voice)  # Run function2 asynchronously

#     def __init__(self):
#         super().__init__()

#         self.pool = multiprocessing.Pool(processes=2)

#         self.setWindowTitle("Waver")
#         self.setGeometry(200, 200, 800, 400)

#         self.button0 = QPushButton("Manual", self)
#         self.button0.setGeometry(0, 0, 800, 60)
#         self.button0.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 25px; }"
#                                     "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 28px;}")
#         self.button0.clicked.connect(self.start_hand_detection)

#         self.button1 = QPushButton("Start Hand\n Detection", self)
#         self.button1.setGeometry(0, 60, 400, 340)
#         self.button1.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px; }"
#                                     "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
#         self.button1.clicked.connect(self.start_hand_detection)
#         # self.button1.setCursor("PointingHandCursor")

#         self.button2 = QPushButton("Start Voice\n Detection", self)
#         self.button2.setGeometry(400, 60, 400, 340)
#         self.button2.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px;}"
#                                     "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
#         self.button2.clicked.connect(self.start_speech_detection)
#         # self.button2.setCursor("PointingHandCursor")
        
#         # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
#         # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
#         # self.setMask(QRegion(self.rect(), QRegion.RegionType.RoundedRect))

#         self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec())
