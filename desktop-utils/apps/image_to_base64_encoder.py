import sys
import base64
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


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded_string


class imageBase64EncoderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to Base64 Encoder")
        self.resize(600, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header label
        self.headerField = QLineEdit("Image to Base64 Encoder")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 24px; font-weight: bold; color: #263238;"
        )
        main_layout.addWidget(self.headerField)

        # Button to select image file
        self.selectButton = QPushButton("Select Image")
        self.selectButton.setStyleSheet(
            """
            QPushButton {
                background-color: #03A9F4;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0288D1;
            }
            """
        )
        self.selectButton.clicked.connect(self.select_image)
        main_layout.addWidget(self.selectButton)

        # Input field to display selected image path (optional)
        self.pathField = QLineEdit()
        self.pathField.setPlaceholderText(
            "Selected image file path will appear here..."
        )
        self.pathField.setReadOnly(True)
        self.pathField.setStyleSheet(
            "padding: 10px; border: 1px solid #B0BEC5; border-radius: 6px; font-size: 16px;"
        )
        main_layout.addWidget(self.pathField)

        # Button to encode image
        self.encodeButton = QPushButton("Encode to Base64")
        self.encodeButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            """
        )
        self.encodeButton.clicked.connect(self.encode_image)
        main_layout.addWidget(self.encodeButton)

        # Output field for Base64 result
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText(
            "Base64 encoded result will be shown here..."
        )
        self.outputField.setStyleSheet(
            "padding: 10px; border: 1px solid #B0BEC5; border-radius: 6px; font-size: 16px; background-color: #FFFFFF;"
        )
        main_layout.addWidget(self.outputField)

        # Horizontal layout for Copy and Save buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.copyButton = QPushButton("Copy Result")
        self.copyButton.setStyleSheet(
            """
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
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
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.saveButton.clicked.connect(self.save_result)
        btn_layout.addWidget(self.saveButton)

        main_layout.addLayout(btn_layout)
        self.setFont(QFont("Arial", 12))

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
        )
        if file_path:
            self.pathField.setText(file_path)
            self.outputField.clear()

    def encode_image(self):
        file_path = self.pathField.text().strip()
        if not file_path:
            QMessageBox.warning(
                self, "Input Error", "Please select an image file first."
            )
            return
        try:
            encoded = image_to_base64(file_path)
            self.outputField.setPlainText(encoded)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Encoding Error",
                f"Failed to encode the image:\n{str(e)}\n{traceback.format_exc()}",
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
    window = imageBase64EncoderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
