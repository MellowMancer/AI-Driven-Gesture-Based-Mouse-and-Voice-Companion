from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPalette, QColor
from voice_main import call_for_voice
from hand_main import call_for_gesture


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Waver")

        self.setGeometry(100, 100, 400, 300)

        self.button1 = QPushButton("Start Hand Detection")
        self.button1.setGeometry(100, 100, 200, 50)
        # self.button1.setStyleSheet("background-color: #3498db; color: white;")
        self.button1.clicked.connect(call_for_gesture)
        # self.button1.setCursor("PointingHandCursor")

        self.button2 = QPushButton("Start Speech Detection")
        self.button2.setGeometry(100, 200, 200, 50)
        # self.button2.setStyleSheet("background-color: #3498db; color: white;")
        self.button2.clicked.connect(call_for_voice)
        # self.button2.setCursor("PointingHandCursor")

        self.show()

        # hand_button = QPushButton("Start Hand Detection")
        # hand_button.setCheckable(True)
        # hand_button.clicked.connect(call_for_gesture)

        # speech_button = QPushButton("Start Speech Detection")
        # speech_button.setCheckable(True)
        # speech_button.clicked.connect(call_for_voice)

        # self.setFixedSize(QSize(600, 400))

        # Set the central widget of the Window.
        # self.setCentralWidget(hand_button)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


app = QApplication([])

# Create a Qt widget, which will be our window.
Waver = MainWindow()
Waver.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()