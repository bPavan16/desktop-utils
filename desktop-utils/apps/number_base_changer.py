import sys
import traceback
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QFileDialog,
    QComboBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Mapping of base names to actual numeric base values
BASE_MAP = {
    "Binary": 2,
    "Octal": 8,
    "Decimal": 10,
    "Hexadecimal": 16,
}


def convert_number(num_str, from_base, to_base):
    # Convert from source base to integer
    num_int = int(num_str, from_base)
    # Convert integer to the target base representation
    if to_base == 2:
        return bin(num_int)
    elif to_base == 8:
        return oct(num_int)
    elif to_base == 10:
        return str(num_int)
    elif to_base == 16:
        return hex(num_int).upper().replace("X", "x")  # standard hex format
    else:
        raise ValueError("Unsupported target base.")


class NumberConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Number Base Changer")
        self.resize(600, 550)
        self.setStyleSheet("background-color: #ECEFF1;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header Label
        self.headerField = QLineEdit("Number Base Changer")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 24px; font-weight: bold; color: #263238;"
        )
        main_layout.addWidget(self.headerField)

        # Input field for the number
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Enter a number (e.g. 1010, FF, 77, etc.)")
        self.inputField.setStyleSheet(
            "padding: 10px; background: white;  border: 1px solid #B0BEC5; border-radius: 6px; font-size: 16px;"
        )
        main_layout.addWidget(self.inputField)

        # Horizontal layout for "From" and "To" selections
        base_layout = QHBoxLayout()
        base_layout.setSpacing(20)

        # From base
        from_layout = QVBoxLayout()
        from_label = QLabel("From Base:")
        from_label.setStyleSheet("font-size: 16px; color: #263238;")
        self.fromComboBox = QComboBox()
        self.fromComboBox.setStyleSheet(
            "padding: 8px; border: 1px solid #B0BEC5; border-radius: 6px; font-size: 16px; background-color: #FFFFFF; color: #263238;"
        )
        self.fromComboBox.addItems(list(BASE_MAP.keys()))
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.fromComboBox)
        base_layout.addLayout(from_layout)

        # To base
        to_layout = QVBoxLayout()
        to_label = QLabel("To Base:")
        to_label.setStyleSheet("font-size: 16px; color: #263238;")
        self.toComboBox = QComboBox()
        self.toComboBox.setStyleSheet(
            "padding: 8px; border: 1px solid #B0BEC5; border-radius: 6px; font-size: 16px; background-color: #FFFFFF; color: #263238;"
        )
        self.toComboBox.addItems(list(BASE_MAP.keys()))
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.toComboBox)
        base_layout.addLayout(to_layout)

        main_layout.addLayout(base_layout)

        # Convert Button
        self.convertButton = QPushButton("Convert")
        self.convertButton.setStyleSheet(
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
        self.convertButton.clicked.connect(self.perform_conversion)
        main_layout.addWidget(self.convertButton)

        # Output field for conversion result
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Conversion result will be shown here...")
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

    def perform_conversion(self):
        num_text = self.inputField.text().strip()
        if not num_text:
            QMessageBox.warning(
                self, "Input Error", "Please enter a number to convert."
            )
            return

        from_base_name = self.fromComboBox.currentText()
        to_base_name = self.toComboBox.currentText()
        from_base = BASE_MAP.get(from_base_name, 10)
        to_base = BASE_MAP.get(to_base_name, 10)

        try:
            result = convert_number(num_text, from_base, to_base)
            self.outputField.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"Failed to convert number:\n{str(e)}\n{traceback.format_exc()}",
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
    window = NumberConverter()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
