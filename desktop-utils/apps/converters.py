import sys
import os
import json
import csv
import yaml
import traceback
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QFileDialog,
    QTextEdit,
)
from PyQt5.QtCore import Qt


def json_to_csv(json_file, csv_file):
    with open(json_file, "r") as jf:
        data = json.load(jf)
    if not isinstance(data, list):
        raise ValueError("JSON data must be a list of objects")
    if len(data) == 0:
        raise ValueError("JSON file is empty")

    with open(csv_file, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=data[0].keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def csv_to_json(csv_file, json_file):
    with open(csv_file, "r") as cf:
        reader = csv.DictReader(cf)
        data = [row for row in reader]
    with open(json_file, "w") as jf:
        json.dump(data, jf, indent=4)


def yaml_to_json(yaml_file, json_file):
    with open(yaml_file, "r") as yf:
        data = yaml.safe_load(yf)
    with open(json_file, "w") as jf:
        json.dump(data, jf, indent=4)


def json_to_yaml(json_file, yaml_file):
    with open(json_file, "r") as jf:
        data = json.load(jf)
    with open(yaml_file, "w") as yf:
        yaml.dump(data, yf, default_flow_style=False)


def csv_to_yaml(csv_file, yaml_file):
    with open(csv_file, "r") as cf:
        reader = csv.DictReader(cf)
        data = [row for row in reader]
    with open(yaml_file, "w") as yf:
        yaml.dump(data, yf, default_flow_style=False)


def yaml_to_csv(yaml_file, csv_file):
    with open(yaml_file, "r") as yf:
        data = yaml.safe_load(yf)
    with open(csv_file, "w", newline="") as cf:
        if isinstance(data, list) and len(data) > 0:
            writer = csv.DictWriter(cf, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        elif isinstance(data, dict):
            writer = csv.writer(cf)
            writer.writerow(list(data.keys()))
            writer.writerow(list(data.values()))
        else:
            raise ValueError("YAML format not recognized for CSV conversion")


class fileConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON, CSV, and YAML Interconverter")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Apply a modern stylesheet
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f7f7f7;
            }
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005f9e;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel {
                color: #333333;
            }
        """
        )

        # Conversion type selection
        self.formatComboBox = QComboBox()
        self.formatComboBox.addItems(
            [
                "JSON to CSV",
                "CSV to JSON",
                "YAML to JSON",
                "JSON to YAML",
                "CSV to YAML",
                "YAML to CSV",
            ]
        )
        self.layout.addWidget(self.formatComboBox)

        # Input file layout: Line edit + Browse button
        input_layout = QHBoxLayout()
        self.inputFileLineEdit = QLineEdit()
        self.inputFileLineEdit.setPlaceholderText("Input file path")
        input_layout.addWidget(self.inputFileLineEdit)
        self.inputBrowseButton = QPushButton("Browse Input")
        self.inputBrowseButton.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.inputBrowseButton)
        self.layout.addLayout(input_layout)

        # File preview area for input file contents
        self.fileContentPreview = QTextEdit()
        self.fileContentPreview.setReadOnly(True)
        self.fileContentPreview.setPlaceholderText("File content preview...")
        self.layout.addWidget(self.fileContentPreview)

        # Output file layout: Line edit + Browse button
        output_layout = QHBoxLayout()
        self.outputFileLineEdit = QLineEdit()
        self.outputFileLineEdit.setPlaceholderText("Output file path")
        output_layout.addWidget(self.outputFileLineEdit)
        self.outputBrowseButton = QPushButton("Browse Output")
        self.outputBrowseButton.clicked.connect(self.select_output_file)
        output_layout.addWidget(self.outputBrowseButton)
        self.layout.addLayout(output_layout)

        # Convert button
        self.convertButton = QPushButton("Convert")
        self.convertButton.clicked.connect(self.perform_conversion)
        self.layout.addWidget(self.convertButton)

        # Status label
        self.statusLabel = QLabel("Status: Ready")
        self.layout.addWidget(self.statusLabel)

    def select_input_file(self):
        file_filter = "All Files (*.*)"
        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "", file_filter
        )
        if selected_file:
            self.inputFileLineEdit.setText(selected_file)
            try:
                with open(selected_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.fileContentPreview.setPlainText(content)
            except Exception as e:
                self.fileContentPreview.setPlainText(f"Error loading file:\n{str(e)}")

    def select_output_file(self):
        file_filter = "All Files (*.*)"
        selected_file, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "", file_filter
        )
        if selected_file:
            self.outputFileLineEdit.setText(selected_file)

    def perform_conversion(self):
        conversion_type = self.formatComboBox.currentText()
        input_path = self.inputFileLineEdit.text().strip()
        output_path = self.outputFileLineEdit.text().strip()

        if not os.path.exists(input_path):
            QMessageBox.warning(self, "Input Error", "Input file does not exist.")
            return

        try:
            if conversion_type == "JSON to CSV":
                json_to_csv(input_path, output_path)
            elif conversion_type == "CSV to JSON":
                csv_to_json(input_path, output_path)
            elif conversion_type == "YAML to JSON":
                yaml_to_json(input_path, output_path)
            elif conversion_type == "JSON to YAML":
                json_to_yaml(input_path, output_path)
            elif conversion_type == "CSV to YAML":
                csv_to_yaml(input_path, output_path)
            elif conversion_type == "YAML to CSV":
                yaml_to_csv(input_path, output_path)
            else:
                raise ValueError("Unsupported conversion type.")

            self.statusLabel.setText("Status: Conversion complete!")
        except Exception as e:
            self.statusLabel.setText("Status: Error during conversion.")
            QMessageBox.critical(
                self,
                "Conversion Error",
                f"An error occurred:\n{str(e)}\n\n{traceback.format_exc()}",
            )


def main():
    app = QApplication(sys.argv)
    window = fileConverterApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
