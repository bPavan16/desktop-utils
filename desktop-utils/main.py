import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QToolBar,
    QAction,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

from apps.color_picker_converter import colorPickerConverterApp
from apps.file_organizer import FileOrganizerApp
from apps.number_base_changer import NumberConverter
from apps.json_formatter import jsonFormatterApp
from apps.url_encoder_decoder import urlEncoderDecoderApp
from apps.query_params import queryParmApp
from apps.converters import fileConverterApp
from apps.image_to_base64_encoder import imageBase64EncoderApp

# List of tool names and their associated icon paths.
TOOLS = [
    ("Format Converter", "icons/format_converter.png"),
    ("File Organizer", "icons/file_organizer.png"),
    ("Query Params to JSON Converter", "icons/query_params.png"),
    ("URL Encoder / Decoder", "icons/url_encoder.png"),
    ("JSON Formatter", "icons/json_formatter.png"),
    ("Color Picker and Converter", "icons/color_picker.png"),
    ("Image to Base64 Encoder", "icons/image_to_base64.png"),
    ("Number Base Changer", "icons/number_base_changer.png"),
]


class HomePage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setStyleSheet("background-color: #fefefe;")

        header = QLabel("Desktop-Utils")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Helvetica", 32, QFont.Bold))
        header.setStyleSheet("color: #333; background-color:transparent")
        layout.addWidget(header)

        grid = QGridLayout()
        grid.setSpacing(50)
        cols = 2
        for index, (tool_name, icon_path) in enumerate(TOOLS):
            card = QPushButton()
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            card.setCursor(Qt.PointingHandCursor)
            card.setStyleSheet(
                """
                QPushButton {
                    background-color: white;
                    border: 2px solid #ddd;
                    border-radius: 15px;
                    padding: 50px;
                }
                QPushButton:hover {
                    background-color: white;
                    border: 2px solid #bbb;
                }
                """
            )

            # Build a layout inside the card.
            v_layout = QVBoxLayout(card)
            v_layout.setSpacing(10)
            v_layout.setAlignment(Qt.AlignCenter)

            # Icon display.
            icon_label = QLabel()
            icon_label.setAlignment(Qt.AlignCenter)
            pix = QPixmap(icon_path)
            if not pix.isNull():
                icon_label.setPixmap(
                    pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
            v_layout.addWidget(icon_label)

            # Tool text.
            text_label = QLabel(tool_name)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont("Helvetica", 16))
            text_label.setStyleSheet("color: #555;")
            v_layout.addWidget(text_label)

            # When clicked, call the switch_callback.
            card.clicked.connect(lambda checked, tn=tool_name: self.switch_callback(tn))
            row = index // cols
            col = index % cols
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()


class ToolPage(QWidget):
    def __init__(self, tool_name, back_callback):
        super().__init__()
        self.tool_name = tool_name
        self.back_callback = back_callback

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setStyleSheet("background-color: #ffffff;")

        header = QLabel(tool_name)
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Helvetica", 28, QFont.Bold))
        header.setStyleSheet("color: #333;")
        layout.addWidget(header)

        # Actual tool UI can replace this placeholder.
        content = QLabel(f"{tool_name} UI will be shown here.")
        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Helvetica", 20))
        content.setStyleSheet("color: #666;")
        layout.addWidget(content)

        # Local Back button (in addition to the global one)
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_button = QPushButton("Back to Dashboard")
        back_button.setFont(QFont("Helvetica", 16))
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setIcon(QIcon("icons/back.png"))
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #03A9F4;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0288D1;
            }
            """
        )
        back_button.clicked.connect(self.back_callback)
        back_layout.addWidget(back_button)
        back_layout.addStretch()

        layout.addLayout(back_layout)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop-Utils")
        self.resize(1100, 800)
        self.setStyleSheet("background-color: #F5F5F5;")

        # Global ToolBar with a Home button.
        toolbar = QToolBar("Global Navigation", self)
        toolbar.setMovable(False)
        toolbar.setStyleSheet("background-color: #eeeeee; padding: 5px;")
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        home_action = QAction(QIcon("icons/back.png"), "Home", self)

        home_action.setToolTip("Back to Dashboard")
        home_action.triggered.connect(self.show_home_page)
        toolbar.addAction(home_action)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self.show_tool_page)
        self.stack.addWidget(self.home_page)

        # Pre-create tool pages.
        number_converter = NumberConverter()
        color_picker_converter = colorPickerConverterApp()
        file_organizer = FileOrganizerApp()
        json_formatter = jsonFormatterApp()
        url_encoder_decoder = urlEncoderDecoderApp()
        query_params_to_json = queryParmApp()
        converter = fileConverterApp()
        image_base64_encoder = imageBase64EncoderApp()

        self.tool_pages = {
            "Number Base Changer": number_converter,
            "Color Picker and Converter": color_picker_converter,
            "File Organizer": file_organizer,
            "JSON Formatter": json_formatter,
            "URL Encoder / Decoder": url_encoder_decoder,
            "Query Params to JSON Converter": query_params_to_json,
            "Format Converter": converter,
            "Image to Base64 Encoder": image_base64_encoder,
        }
        self.stack.addWidget(number_converter)
        self.stack.addWidget(color_picker_converter)
        self.stack.addWidget(file_organizer)
        self.stack.addWidget(json_formatter)
        self.stack.addWidget(url_encoder_decoder)
        self.stack.addWidget(query_params_to_json)
        self.stack.addWidget(converter)
        self.stack.addWidget(image_base64_encoder)

    def show_tool_page(self, tool_name):
        if tool_name not in self.tool_pages:
            page = ToolPage(tool_name, self.show_home_page)
            self.tool_pages[tool_name] = page
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(self.tool_pages[tool_name])

    def show_home_page(self):
        self.stack.setCurrentWidget(self.home_page)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
