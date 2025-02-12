import sys
import urllib.parse
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
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt


def url_encode(text):
    return urllib.parse.quote(text)


def url_decode(text):
    return urllib.parse.unquote(text)


class urlEncoderDecoderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Encoder / Decoder")
        self.resize(600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header label
        self.headerField = QLineEdit("URL Encoder / Decoder")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(self.headerField)

        # Text input field
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter URL string to encode or decode...")
        self.inputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.inputField)

        # Buttons layout: Encode and Decode
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.encodeButton = QPushButton("Encode")
        self.encodeButton.setStyleSheet(
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
        self.encodeButton.clicked.connect(self.perform_encode)
        action_layout.addWidget(self.encodeButton)

        self.decodeButton = QPushButton("Decode")
        self.decodeButton.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            """
        )
        self.decodeButton.clicked.connect(self.perform_decode)
        action_layout.addWidget(self.decodeButton)

        main_layout.addLayout(action_layout)

        # Output display field for result
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Result will be shown here...")
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

    def perform_encode(self):
        text = self.inputField.text().strip()
        if not text:
            QMessageBox.warning(
                self, "Input Error", "Please enter a URL string to encode."
            )
            return
        try:
            result = url_encode(text)
            self.outputField.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Encode Error",
                f"An error occurred while encoding:\n{str(e)}\n{traceback.format_exc()}",
            )

    def perform_decode(self):
        text = self.inputField.text().strip()
        if not text:
            QMessageBox.warning(
                self, "Input Error", "Please enter a URL string to decode."
            )
            return
        try:
            result = url_decode(text)
            self.outputField.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Decode Error",
                f"An error occurred while decoding:\n{str(e)}\n{traceback.format_exc()}",
            )

    def copy_result(self):
        result_text = self.outputField.toPlainText()
        if not result_text:
            QMessageBox.information(self, "Copy Result", "No result available to copy.")
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(result_text)
        QMessageBox.information(self, "Copy Result", "Result copied to clipboard.")

    def save_result(self):
        result_text = self.outputField.toPlainText()
        if not result_text:
            QMessageBox.information(self, "Save Result", "No result available to save.")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Result To File", "", "Text Files (*.txt);;All Files (*)"
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
    window = urlEncoderDecoderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
