from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)
import sys

class MetaView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetaView")
        self.setMinimumSize(QSize(400, 550))
        
        layout = QHBoxLayout()
        layoutV1 = QVBoxLayout()
        layoutV2 = QVBoxLayout()
        
        layout.addLayout(layoutV1)
        layout.addLayout(layoutV2)
        
        self.button1 = QPushButton("Click me!")
        self.button1.clicked.connect(self.clicked_button1)
        
        self.button2 = QPushButton("Click me!")
        self.button2.clicked.connect(self.clicked_button2)
        
        layoutV1.addWidget(self.button1, alignment=Qt.AlignTop)
        layoutV2.addWidget(self.button2, alignment=Qt.AlignTop)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def clicked_button1(self):
        print("Clicked button 1")
    
    def clicked_button2(self):
        print("Clicked button 2")

def main():
    app = QApplication(sys.argv)

    window = MetaView()
    window.show()

    app.exec()