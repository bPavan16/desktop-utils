import sys
import urllib.parse
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
from PyQt5.QtGui import QClipboard, QFont
from PyQt5.QtCore import Qt


def query_params_to_json(query_string):
    # Parse the query string into a dictionary
    parsed_params = urllib.parse.parse_qs(query_string)
    # Convert the dictionary to a JSON object
    json_object = {key: value[0] for key, value in parsed_params.items()}
    return json.dumps(json_object, indent=4)


class queryParmApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Query Params to JSON Converter")
        self.resize(600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header label for a polished look (using QLineEdit as a label)
        self.headerField = QLineEdit("Query Params to JSON Converter")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(self.headerField)

        # Query string input field
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText(
            "Enter query parameters (e.g. foo=bar&baz=qux)"
        )
        self.inputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.inputField)

        # Convert button
        self.convertButton = QPushButton("Convert")
        self.convertButton.setStyleSheet(
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
        self.convertButton.clicked.connect(self.convert_query)
        main_layout.addWidget(self.convertButton)

        # Output display field for JSON result
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Converted JSON will be shown here...")
        self.outputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.outputField)

        # Horizontal layout for Copy and Save buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.copyButton = QPushButton("Copy JSON")
        self.copyButton.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            """
        )
        self.copyButton.clicked.connect(self.copy_json)
        btn_layout.addWidget(self.copyButton)

        self.saveButton = QPushButton("Save JSON")
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
        self.saveButton.clicked.connect(self.save_json)
        btn_layout.addWidget(self.saveButton)

        main_layout.addLayout(btn_layout)

        # Set general application font
        self.setFont(QFont("Arial", 10))

    def convert_query(self):
        query_string = self.inputField.text().strip()
        if not query_string:
            QMessageBox.warning(self, "Input Error", "Please enter query parameters.")
            return

        try:
            json_result = query_params_to_json(query_string)
            self.outputField.setPlainText(json_result)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"An error occurred:\n{str(e)}\n\n{traceback.format_exc()}",
            )

    def copy_json(self):
        json_text = self.outputField.toPlainText()
        if not json_text:
            QMessageBox.information(self, "Copy JSON", "No JSON available to copy.")
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(json_text, mode=QClipboard.Clipboard)
        clipboard.setText(json_text, mode=QClipboard.Selection)
        QMessageBox.information(self, "Copy JSON", "JSON copied to clipboard.")

    def save_json(self):
        json_text = self.outputField.toPlainText()
        if not json_text:
            QMessageBox.information(self, "Save JSON", "No JSON available to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save JSON To File", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(json_text)
                QMessageBox.information(
                    self, "Save JSON", f"JSON saved to {file_path}."
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Save JSON", f"Failed to save JSON:\n{str(e)}"
                )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = queryParmApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
