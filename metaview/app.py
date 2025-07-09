from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MetaView")
        button = QPushButton("Click me!")
        
        self.setCentralWidget(button)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()