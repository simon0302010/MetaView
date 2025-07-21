import logging
import os
import re
import sys

import importlib.resources

from colorama import Fore, Style, init
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFontMetrics, QPixmap, QTransform, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import exiftool, extra_data, location, weather
from .earth import EarthWidget

READ_ONLY_KEYS = {
    "Source File",
    "File Name",
    "Directory",
    "File Size",
    "File Permissions",
    "Location",
    "Image Size",
    "File Type",
    "Megapixels",
    "Temperature",
    "Weather",
}

# TODO: better styling for cli

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.clicked.emit()
        super().mouseDoubleClickEvent(event)


TRUNCATION_LENGTH = 30

class MetaView(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.setWindowTitle("MetaView")
        self.setMinimumSize(QSize(500, 600))
        with importlib.resources.path("metaview.assets", "MetaView128.png") as icon_path:
            self.setWindowIcon(QIcon(str(icon_path)))

        label = QLabel("Open a file to get started.")
        label.setAlignment(Qt.AlignCenter)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        open_action = file_menu.addAction("Open")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        quit_action = file_menu.addAction("Quit")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit)

        save_action = file_menu.addAction("Save")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_metadata)

        save_to_action = file_menu.addAction("Save to")
        save_to_action.setShortcut("Ctrl+Shift+S")
        save_to_action.triggered.connect(self.save_to)

        delete_metadata_action = file_menu.addAction("Delete Metadata")
        delete_metadata_action.setShortcut("Ctrl+Del")
        delete_metadata_action.triggered.connect(self.delete_metadata)

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
        if not self.file_path or not os.path.exists(self.file_path):
            return
        
        valid_exts = (".jpg", ".jpeg", ".png")
        if not self.file_path.lower().endswith(valid_exts):
            self.display_error("Only .jpg, .jpeg, and .png files are supported (More are to be tested).")
            return

        logging.info(f"Selected File: {self.file_path}")

        self.metadata = exiftool.get_metadata(self.file_path)
        self.original_backend_keys = set(self.metadata.keys())
        self.original_values = {}

        logging.debug(self.metadata)

        # format values better
        if "GPSImgDirection" in self.metadata:
            self.metadata["GPSImgDirection"] = round(
                self.metadata["GPSImgDirection"], 2
            )
        if "GPSSpeed" in self.metadata:
            self.metadata["GPSSpeed"] = round(
                self.metadata["GPSSpeed"], 2
            )
        if "ThumbnailImage" in self.metadata:
            del self.metadata["ThumbnailImage"]

        self.categories_dict = extra_data.categories_dict

        self.categories = self.categorize_metadata(self.metadata)

        for cat, items in self.categories.items():
            for display_key, value in items.items():
                if isinstance(value, str):
                    backend_key = self.display_to_backend.get(cat, {}).get(display_key)
                    if backend_key:
                        self.original_values[backend_key] = value

        # add preview image
        image_label = QLabel()
        pixmap = QPixmap(self.file_path)

        if "Orientation" in self.metadata:
            orientation = self.metadata["Orientation"]
            logging.debug(f"Orientation: {orientation}")
            re_result = re.findall("(\d+)", str(orientation))
            if len(re_result):
                orientation = int(re_result[0])
                im_transform = QTransform()
                im_transform.rotate(90)
                pixmap = pixmap.transformed(im_transform)

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

        # add location as text
        if "GPSLatitude" in self.metadata and "GPSLongitude" in self.metadata:
            GPSLatitude = self.metadata["GPSLatitude"]
            GPSLongitude = self.metadata["GPSLongitude"]
            GPSLatitude = location.convert_dms(GPSLatitude)
            GPSLongitude = location.convert_dms(GPSLongitude)

            city, region, country = location.get_location(GPSLatitude, GPSLongitude)

            location_str = f"{city}, {region}, {country}"

            self.add_property("Location", "Location", location_str)

            earth_widget = EarthWidget(GPSLatitude, GPSLongitude)
            earth_widget.setMaximumHeight(256)
            self.add_property("Location", "Earth View", earth_widget)

            if "DateTimeOriginal" in self.metadata:
                temperature, weather_str = weather.get_weather(
                    self.metadata["DateTimeOriginal"], GPSLatitude, GPSLongitude
                )

                self.add_property("Date && Time", "Temperature", temperature)
                self.add_property("Date && Time", "Weather", weather_str)

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

            def make_label(text, layoutH, key, cat=category):  # Capture category
                label = ClickableLabel(text)
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                def on_label_clicked():
                    if key in READ_ONLY_KEYS:
                        self.display_error("You can't edit this.")
                        return
                    line_edit = QLineEdit(label.text())
                    line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                    # adaptive width
                    def adjust_width():
                        fm = QFontMetrics(line_edit.font())
                        text_width = fm.horizontalAdvance(line_edit.text() or " ")
                        line_edit.setMinimumWidth(text_width + 20)

                    line_edit.textChanged.connect(adjust_width)
                    adjust_width()

                    idx = layoutH.indexOf(label)
                    layoutH.removeWidget(label)
                    label.deleteLater()
                    layoutH.insertWidget(
                        idx, line_edit, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter
                    )

                    def finish_edit():
                        new_text = line_edit.text()
                        # Update the categories data structure
                        self.categories[cat][key] = new_text

                        new_label = make_label(new_text, layoutH, key, cat)
                        layoutH.removeWidget(line_edit)
                        line_edit.deleteLater()
                        layoutH.insertWidget(
                            idx, new_label, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter
                        )

                    line_edit.editingFinished.connect(finish_edit)
                    line_edit.setFocus()

                label.clicked.connect(on_label_clicked)
                return label

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
                    value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    layoutH.addWidget(
                        value, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter
                    )
                else:
                    label2 = make_label(str(value), layoutH, key)
                    layoutH.addWidget(
                        label2, 1, alignment=Qt.AlignLeft | Qt.AlignVCenter
                    )

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
        new_title = self.file_path
        if len(new_title) >= TRUNCATION_LENGTH:
            new_title = "..." + new_title[-TRUNCATION_LENGTH:]
        new_title = f"MetaView ({new_title})"
        self.setWindowTitle(new_title)

    def categorize_metadata(self, metadata):
        categories = {cat: {} for cat in self.categories_dict}
        display_to_backend = {cat: {} for cat in self.categories_dict}
        uncategorized = {}
        uncategorized_map = {}

        for key, value in metadata.items():
            display_key = extra_data.rename_dict.get(key, key)
            found = False
            for cat, keys in self.categories_dict.items():
                if key in keys:
                    # unique display keys
                    orig_display_key = display_key
                    i = 1
                    while display_key in categories[cat]:
                        display_key = f"{orig_display_key} ({i})"
                        i += 1
                    categories[cat][display_key] = value
                    display_to_backend[cat][display_key] = key
                    found = True
                    break
            if not found:
                orig_display_key = display_key
                i = 1
                while display_key in uncategorized:
                    display_key = f"{orig_display_key} ({i})"
                    i += 1
                uncategorized[display_key] = value
                uncategorized_map[display_key] = key

        if uncategorized:
            categories["Other"] = uncategorized
            display_to_backend["Other"] = uncategorized_map

        categories = {cat: items for cat, items in categories.items() if items}
        display_to_backend = {
            cat: items for cat, items in display_to_backend.items() if items
        }
        self.display_to_backend = display_to_backend
        return categories

    def add_property(self, category, property, value):
        self.categories.setdefault(str(category), {})[str(property)] = value

    def remove_property(self, category, property):
        if (
            str(category) in self.categories
            and str(property) in self.categories[str(category)]
        ):
            del self.categories[str(category)][str(property)]
        else:
            logging.warning(
                f"Unable to delete property '{property}' from category '{category}': Property does not exist."
            )

    def update_property(self, category, property, value):
        if (
            str(category) in self.categories
            and str(property) in self.categories[str(category)]
        ):
            self.categories[str(category)][str(property)] = value
        else:
            logging.warning(
                f"Unable to update property '{property}' from category '{category}': Property does not exist."
            )

    def display_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()

    def save_to(self, backup=False):
        filter = "Images (*.jpg *.jpeg *.png)"
        dialog = QFileDialog(self, "Save to")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(filter)
        if dialog.exec_():
            file_paths = dialog.selectedFiles()
            for single_path in file_paths:
                if os.path.exists(single_path):
                    self.save_metadata(everything=True, save_path=single_path)
                    logging.info(f"Saved metadata to {single_path}")
                    if os.path.exists(f"{single_path}_original") and not backup:
                        logging.debug("Deleting backup of modified photo.")
                        os.remove(f"{single_path}_original")

    def pre_save(self, everything=False):
        new_data = {}
        for cat, items in self.categories.items():
            for display_key, value in items.items():
                # only update strings
                if isinstance(value, (str, int, float)):
                    backend_key = self.display_to_backend.get(cat, {}).get(display_key)
                    # skip keys that were added afterwards and check if value changed
                    if (
                        backend_key
                        and backend_key in self.original_backend_keys
                        and display_key not in READ_ONLY_KEYS
                        and backend_key not in READ_ONLY_KEYS
                        and self.original_values.get(backend_key)
                        != value  # only changed values
                    ):
                        new_data[backend_key] = value
                        logging.debug(
                            f"{display_key}: {self.original_values.get(backend_key)} -> {value}"
                        )

                    elif (
                        backend_key
                        and backend_key in self.original_backend_keys
                        and backend_key not in READ_ONLY_KEYS
                        and display_key not in READ_ONLY_KEYS
                        and not backend_key == "Orientation"
                        and everything
                    ):
                        new_data[backend_key] = value
                        logging.debug(
                            f"{display_key}: {self.original_values.get(backend_key)} -> {value}"
                        )
        return new_data

    def save_metadata(self, everything=False, save_path=None):
        logging.info("Saving new metadata...")
        new_data = self.pre_save(everything=everything)
        if save_path:
            result = exiftool.write_metadata(save_path, new_data)
        else:
            result = exiftool.write_metadata(self.file_path, new_data)
        logging.info(result)

    def delete_metadata(self, backup=False):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Do you really want to delete all metadata from the image?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            exiftool.delete_metadata(self.file_path)
            print(f"Deleted all metadata from {self.file_path}")
            if os.path.exists(f"{self.file_path}_original") and not backup:
                logging.debug("Deleting backup of modified photo.")
                os.remove(f"{self.file_path}_original")
            self.open_file(self.file_path)

    def quit(self):
        logging.info("Quitting...")
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    try:
        window = MetaView(sys.argv[1])
    except IndexError:
        window = MetaView()
    window.show()
    app.exec()
