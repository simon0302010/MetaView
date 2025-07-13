import json
import subprocess
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import extra_data


class MetaView(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("MetaView")
        self.setMinimumSize(QSize(400, 550))

        label = QLabel("Open a file to get started.")
        label.setAlignment(Qt.AlignCenter)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)

        self.setCentralWidget(label)

        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path=None):
        if file_path:
            self.file_path = file_path
        else:
            self.file_path, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "Images (*.jpg *.jpeg *.png)"
            )
        if not self.file_path:
            return

        print(f"Selected File: {self.file_path}")

        self.metadata = self.get_metadata()

        self.categories_dict = extra_data.categories_dict

        self.categories = self.categorize_metadata(self.metadata)

        tab_widget = QTabWidget()
        for category, items in self.categories.items():
            widget = QWidget()
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)

            # Header
            layoutH = QHBoxLayout()
            label1 = QLabel("Property")
            label2 = QLabel("Value")
            label1.setStyleSheet("font-weight: bold; font-size: 15px;")
            label2.setStyleSheet("font-weight: bold; font-size: 15px;")
            layoutH.addWidget(label1, alignment=Qt.AlignVCenter)
            layoutH.addWidget(label2, alignment=Qt.AlignVCenter)
            layout.addLayout(layoutH)
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: gray; background-color: gray;")
            line.setFixedHeight(2)
            layout.addWidget(line)

            for key, value in items.items():
                row_widget = QWidget()
                row_layout = QVBoxLayout()
                row_layout.setSpacing(0)
                row_layout.setContentsMargins(0, 0, 0, 0)

                layoutH = QHBoxLayout()
                layoutH.setSpacing(10)
                layoutH.setContentsMargins(8, 0, 8, 0)
                label1 = QLabel(str(key))
                label2 = QLabel(str(value))
                layoutH.addWidget(label1, alignment=Qt.AlignVCenter)
                layoutH.addWidget(label2, alignment=Qt.AlignVCenter)
                row_layout.addLayout(layoutH)

                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setStyleSheet("color: gray; background-color: gray;")
                line.setFixedHeight(1)
                row_layout.addWidget(line)

                row_widget.setLayout(row_layout)
                row_widget.setMinimumHeight(32)
                layout.addWidget(row_widget)

            layout.addStretch()
            widget.setLayout(layout)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(widget)
            tab_widget.addTab(scroll, category)

        self.setCentralWidget(tab_widget)

    def categorize_metadata(self, metadata):
        categories = {cat: {} for cat in self.categories_dict}
        uncategorized = {}

        for key, value in metadata.items():
            found = False
            for cat, keys in self.categories_dict.items():
                if key in keys:
                    categories[cat][key] = value
                    found = True
                    break
            if not found:
                uncategorized[key] = value

        if uncategorized:
            categories["Other"] = uncategorized

        categories = {cat: items for cat, items in categories.items() if items}
        return categories

    def get_metadata(self, file_path=None):
        if file_path:
            pass
        elif hasattr(self, "file_path"):
            file_path = self.file_path
        else:
            print("Please load a file first.")
            return

        result = subprocess.run(
            ["exiftool", "-j", self.file_path], capture_output=True, text=True
        )
        self.metadata = json.loads(result.stdout)
        return self.metadata[0] if self.metadata else {}


def main():
    app = QApplication(sys.argv)
    try:
        window = MetaView(sys.argv[1])
    except IndexError:
        window = MetaView()
    window.show()
    app.exec()
