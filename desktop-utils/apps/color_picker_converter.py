import sys
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
    QColorDialog,
    QComboBox,
)
from PyQt5.QtGui import QColor, QFont, QClipboard
from PyQt5.QtCore import Qt


def hex_to_rgb(hex_str):
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) != 6:
        raise ValueError("HEX color must be 6 characters long.")
    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
    except Exception as e:
        raise ValueError("Invalid HEX color code.") from e
    return f"rgb({r}, {g}, {b})"


def rgb_to_hex(rgb_str):
    # Expecting input as "r, g, b" or "r g b"
    parts = (
        rgb_str.replace("(", "")
        .replace(")", "")
        .replace("rgb", "")
        .replace(",", " ")
        .split()
    )
    if len(parts) != 3:
        raise ValueError("RGB input must have three components.")
    try:
        r, g, b = [int(part) for part in parts]
        if not all(0 <= x <= 255 for x in [r, g, b]):
            raise ValueError("RGB values must be in the range 0-255.")
    except Exception as e:
        raise ValueError("Invalid RGB input.") from e
    return f"#{r:02X}{g:02X}{b:02X}"


class colorPickerConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Picker and Converter")
        self.resize(600, 550)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header label
        self.headerField = QLineEdit("Color Picker and Converter")
        self.headerField.setReadOnly(True)
        self.headerField.setAlignment(Qt.AlignCenter)
        self.headerField.setStyleSheet(
            "background: transparent; border: none; font-size: 20px; font-weight: bold;"
        )
        main_layout.addWidget(self.headerField)

        # Color Picker button
        self.pickColorButton = QPushButton("Pick a Color")
        self.pickColorButton.setStyleSheet(
            """
            QPushButton {
                background-color: #FFC107;
                color: black;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
            """
        )
        self.pickColorButton.clicked.connect(self.pick_color)
        main_layout.addWidget(self.pickColorButton)

        # Input field for color code
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText(
            "Enter HEX (e.g. #FF5733) or RGB (e.g. 255,87,51)"
        )
        self.inputField.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        main_layout.addWidget(self.inputField)

        # ComboBox for selecting conversion direction
        self.conversionComboBox = QComboBox()
        self.conversionComboBox.setStyleSheet(
            "padding: 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;"
        )
        self.conversionComboBox.addItems(["HEX to RGB", "RGB to HEX"])
        main_layout.addWidget(self.conversionComboBox)

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
        self.convertButton.clicked.connect(self.perform_conversion)
        main_layout.addWidget(self.convertButton)

        # Output display field for conversion result
        self.outputField = QTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Conversion result will be shown here...")
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

        self.setFont(QFont("Arial", 10))

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # Display the selected color's HEX in the inputField
            self.inputField.setText(color.name().upper())
            # Also show the RGB value in the output field
            self.outputField.setPlainText(
                f"rgb({color.red()}, {color.green()}, {color.blue()})"
            )

    def perform_conversion(self):
        text = self.inputField.text().strip()
        if not text:
            QMessageBox.warning(
                self, "Input Error", "Please enter a color value or pick one."
            )
            return
        conversion = self.conversionComboBox.currentText()
        try:
            if conversion == "HEX to RGB":
                result = hex_to_rgb(text)
            elif conversion == "RGB to HEX":
                result = rgb_to_hex(text)
            else:
                result = "Unknown conversion operation."
            self.outputField.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Conversion Error", f"Error: {str(e)}")

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
    window = colorPickerConverterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
