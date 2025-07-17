from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import sys

class FileDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Demo")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        self.label = QLabel("No files selected.")
        self.button = QPushButton("Open Files")
        self.button.clicked.connect(self.loadFiles)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def loadFiles(self):
        filter = "Images (*.jpg *.jpeg *.png)"
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter(filter)
        if dialog.exec_():
            names = dialog.selectedFiles()
            print(names)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = FileDialogDemo()
    demo.show()
    sys.exit(app.exec_())