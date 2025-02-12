import sys
import json
import traceback
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def format_json(text):
    # Parse the JSON to validate and format it with indentation
    parsed = json.loads(text)
    return json.dumps(parsed, indent=4)


class jsonFormatterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Formatter")
        self.resize(600, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header label
        self.headerField = QLineEdit("JSON Formatter")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(self.headerField)

        # Load JSON button
        self.loadButton = QPushButton("Load JSON from File")
        self.loadButton.setStyleSheet(
            """
            QPushButton {
                background-color: #03A9F4;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0288D1;
            }
            """
        )
        self.loadButton.clicked.connect(self.load_json)
        main_layout.addWidget(self.loadButton)

        # Input field for raw JSON
        self.inputField = QTextEdit()
        self.inputField.setPlaceholderText("Paste your JSON here...")
        self.inputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.inputField)

        # Format button
        self.formatButton = QPushButton("Format JSON")
        self.formatButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.formatButton.clicked.connect(self.perform_format)
        main_layout.addWidget(self.formatButton)

        # Output field for formatted JSON
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Formatted JSON will be shown here...")
        self.outputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.outputField)

        # Horizontal layout for Copy and Save buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.copyButton = QPushButton("Copy Result")
        self.copyButton.setStyleSheet(
            """
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            """
        )
        self.copyButton.clicked.connect(self.copy_result)
        btn_layout.addWidget(self.copyButton)

        self.saveButton = QPushButton("Save Result")
        self.saveButton.setStyleSheet(
            """
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            """
        )
        self.saveButton.clicked.connect(self.save_result)
        btn_layout.addWidget(self.saveButton)

        main_layout.addLayout(btn_layout)

        # Set application font
        self.setFont(QFont("Arial", 10))

    def load_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON File",
            "",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)",
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.inputField.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(
                    self, "Load Error", f"Failed to load JSON from file:\n{str(e)}"
                )

    def perform_format(self):
        raw_text = self.inputField.toPlainText().strip()
        if not raw_text:
            QMessageBox.warning(
                self, "Input Error", "Please paste valid JSON to format."
            )
            return
        try:
            formatted_json = format_json(raw_text)
            self.outputField.setPlainText(formatted_json)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Format Error",
                f"An error occurred while formatting JSON:\n{str(e)}\n{traceback.format_exc()}",
            )

    def copy_result(self):
        result_text = self.outputField.toPlainText()
        if not result_text:
            QMessageBox.information(self, "Copy Result", "No result available to copy.")
            return
        QApplication.clipboard().setText(result_text)
        QMessageBox.information(self, "Copy Result", "Result copied to clipboard.")

    def save_result(self):
        result_text = self.outputField.toPlainText()
        if not result_text:
            QMessageBox.information(self, "Save Result", "No result available to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Result To File",
            "",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)",
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(result_text)
                QMessageBox.information(
                    self, "Save Result", f"Result saved to {file_path}."
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Save Result", f"Failed to save result:\n{str(e)}"
                )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = jsonFormatterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
