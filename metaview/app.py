from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QFrame,
    QScrollArea,
    QFileDialog
)
import sys

class MetaView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetaView")
        self.setMinimumSize(QSize(400, 550))
        
        self.layoutV = QVBoxLayout()
        self.layoutV.setSpacing(0)
        self.layoutV.setContentsMargins(0,0,0,0)
        self.text_rows = []
        
        label = QLabel("Open a file to get started.")
        label.setAlignment(Qt.AlignCenter)
        
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        
        self.setCentralWidget(label)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )
        if not file_path:
            return

        self.add_text_row("Property", "Value")

        for i in range(5):
            self.add_text_row(str(i), str(i))

        self.layoutV.addStretch()

        content_widget = QWidget()
        content_widget.setLayout(self.layoutV)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        
        self.setCentralWidget(scroll)

    def add_text_row(self, text1="", text2=""):
        row_widget = QWidget()
        row_layout = QVBoxLayout()
        row_layout.setSpacing(0)
        row_layout.setContentsMargins(0, 0, 0, 0)

        layoutH = QHBoxLayout()
        layoutH.setSpacing(10)
        layoutH.setContentsMargins(8, 0, 8, 0)
        label1 = QLabel(text1)
        label2 = QLabel(text2)
        layoutH.addWidget(label1, alignment=Qt.AlignVCenter)
        layoutH.addWidget(label2, alignment=Qt.AlignVCenter)
        row_layout.addLayout(layoutH)

        # separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: gray; background-color: gray;")
        line.setFixedHeight(2)
        row_layout.addWidget(line)

        row_widget.setLayout(row_layout)
        row_widget.setMinimumHeight(32)

        self.layoutV.addWidget(row_widget)
        self.text_rows.append((label1, label2))

def main():
    app = QApplication(sys.argv)
    window = MetaView()
    window.show()
    app.exec()