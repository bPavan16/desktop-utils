import os
import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon


class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window set-up
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 1100, 750)
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ece9e6, stop:1 #ffffff);
            }
            QLabel {
                font-family: 'Segoe UI';
                color: #333;
            }
            QStatusBar {
                background: #ececec;
                color: #555;
                padding: 8px;
            }
            QFrame {
                background: #fff;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #ddd;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTreeWidget {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px;
            }
            QTreeWidget::item {
                padding: 6px;
            }
        """
        )

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Title label with medium text
        title_label = QLabel("File Organizer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title_label)

        # Container for buttons with a frame
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(15, 15, 15, 15)
        button_layout.setSpacing(20)

        # Source folder label with medium font
        self.source_label = QLabel("No folder selected")
        self.source_label.setStyleSheet(
            """
            padding: 8px;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 4px;
        """
        )
        self.source_label.setFont(QFont("Segoe UI", 14))
        self.source_label.setMinimumWidth(400)

        # Select folder button with medium icon & text
        self.select_button = QPushButton("📁 Select Folder")
        self.select_button.setFont(QFont("Segoe UI", 14))
        # Uncomment and provide path if a custom icon is available
        # self.select_button.setIcon(QIcon("path/to/folder_icon.png"))
        # self.select_button.setIconSize(QSize(20, 20))
        self.select_button.clicked.connect(self.select_folder)

        # Organize files button with medium icon & text
        self.organize_button = QPushButton("🗂 Organize Files")
        self.organize_button.setFont(QFont("Segoe UI", 14))
        # Uncomment and provide path if a custom icon is available
        # self.organize_button.setIcon(QIcon("path/to/organize_icon.png"))
        # self.organize_button.setIconSize(QSize(20, 20))
        self.organize_button.clicked.connect(self.organize_files)

        button_layout.addWidget(self.source_label, 1)
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.organize_button)
        main_layout.addWidget(button_container)

        # Files tree widget with moderate font for readability
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Files and Folders"])
        self.tree_widget.setFont(QFont("Segoe UI", 13))
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setAnimated(True)
        main_layout.addWidget(self.tree_widget)

        self.source_path = None

        # StatusBar setup
        self.statusBar().showMessage("Ready")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.source_path = folder
            self.source_label.setText(f"Selected: {folder}")
            self.display_files()

    def display_files(self):
        self.tree_widget.clear()
        if not self.source_path:
            return

        root = QTreeWidgetItem(self.tree_widget, [self.source_path])
        self._populate_tree(self.source_path, root)
        self.tree_widget.expandAll()

    def _populate_tree(self, path, parent):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                tree_item = QTreeWidgetItem(parent, [item])
                if os.path.isdir(item_path):
                    self._populate_tree(item_path, tree_item)
        except Exception as e:
            print(f"Error populating tree: {e}")

    def organize_files(self):
        if not self.source_path:
            QMessageBox.warning(self, "Warning", "Please select a folder first!")
            return

        try:
            # Get all files in the source directory
            files = [
                f
                for f in os.listdir(self.source_path)
                if os.path.isfile(os.path.join(self.source_path, f))
            ]

            # Group files by extension and move them
            for file in files:
                extension = os.path.splitext(file)[1][1:].lower() or "no_extension"
                ext_dir = os.path.join(self.source_path, extension)
                if not os.path.exists(ext_dir):
                    os.makedirs(ext_dir)
                source_file = os.path.join(self.source_path, file)
                destination_file = os.path.join(ext_dir, file)
                shutil.move(source_file, destination_file)

            QMessageBox.information(self, "Success", "Files organized successfully!")
            self.display_files()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
