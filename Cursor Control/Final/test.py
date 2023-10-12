import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QFont, QColor, QPainter, QRegion
from PyQt6.QtCore import Qt, QRectF
from voice_main import call_for_voice
from hand_main import call_for_gesture
import multiprocessing

class MainWindow(QMainWindow):

    def start_hand_detection(self):
        self.pool.apply_async(call_for_gesture)  # Run function1 asynchronously

    def start_speech_detection(self):
        self.pool.apply_async(call_for_voice)  # Run function2 asynchronously

    def __init__(self):
        super().__init__()

        self.pool = multiprocessing.Pool(processes=2)

        self.setWindowTitle("Waver")
        self.setGeometry(200, 200, 800, 400)

        self.button0 = QPushButton("Manual", self)
        self.button0.setGeometry(0, 0, 800, 60)
        self.button0.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 25px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 28px;}")
        self.button0.clicked.connect(self.start_hand_detection)

        self.button1 = QPushButton("Start Hand\n Detection", self)
        self.button1.setGeometry(0, 60, 400, 340)
        self.button1.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px; }"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
        self.button1.clicked.connect(self.start_hand_detection)
        # self.button1.setCursor("PointingHandCursor")

        self.button2 = QPushButton("Start Voice\n Detection", self)
        self.button2.setGeometry(400, 60, 400, 340)
        self.button2.setStyleSheet("QPushButton { background-color: #262529; color: white; font: bold 30px;}"
                                    "QPushButton:hover { background-color: #262529; color: #f02e61; font: bold 35px;}")
        self.button2.clicked.connect(self.start_speech_detection)
        # self.button2.setCursor("PointingHandCursor")
        
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # self.setMask(QRegion(self.rect(), QRegion.RegionType.RoundedRect))

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
