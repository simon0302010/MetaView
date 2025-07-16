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
from PyQt5.QtGui import QPixmap

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

        quit_actoin = file_menu.addAction("Quit")
        quit_actoin.triggered.connect(self.quit)

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
        
        # add preview image
        image_label = QLabel()
        pixmap = QPixmap(self.file_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        max_height = 128
        image_label.setMaximumHeight(max_height)

        if not pixmap.isNull():
            aspect_ratio = pixmap.width() / pixmap.height()
            width = int(max_height * aspect_ratio)
            image_label.setMaximumWidth(width)
        else:
            image_label.setMaximumWidth(max_height)  # fallback if pixmap is invalid

        self.add_property("General", "Image Preview", image_label)

        tab_widget = QTabWidget()
        for category, items in self.categories.items():
            widget = QWidget()
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)

            # Header
            layoutH = QHBoxLayout()
            label1 = QLabel(" Property")
            label2 = QLabel("   Value")
            label1.setStyleSheet("font-weight: bold; font-size: 15px;")
            label2.setStyleSheet("font-weight: bold; font-size: 15px;")
            label1.setFixedWidth(200)
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
                label1.setFixedWidth(200)
                layoutH.addWidget(label1, alignment=Qt.AlignVCenter)

                if isinstance(value, QWidget):
                    layoutH.addWidget(value, alignment=Qt.AlignVCenter | Qt.AlignLeft)
                else:
                    label2 = QLabel(str(value))
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
            display_key = extra_data.rename_dict.get(key, key)
            found = False
            for cat, keys in self.categories_dict.items():
                if key in keys:
                    categories[cat][display_key] = value
                    found = True
                    break
            if not found:
                uncategorized[display_key] = value

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

    def add_property(self, category, property, value):
        self.categories.setdefault(str(category), {})[str(property)] = value

    def remove_property(self, category, property):
        if str(category) in self.categories and str(property) in self.categories[str(category)]:
            del self.categories[str(category)][str(property)]
        else:
            print(f"Unable to delete property '{property}' from category '{category}': Property does not exist.")
    
    def update_property(self, category, property, value):
        if str(category) in self.categories and str(property) in self.categories[str(category)]:
            self.categories[str(category)][str(property)] = value
        else:
            print(f"Unable to update property '{property}' from category '{category}': Property does not exist.")
    
    def quit(self):
        print("Quitting...")
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    try:
        window = MetaView(sys.argv[1])
    except IndexError:
        window = MetaView()
    window.show()
    app.exec()
