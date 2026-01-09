import os

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QTextEdit,
                               QSizePolicy, QStyle, QLineEdit)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QCloseEvent

class MainWindow(QMainWindow):
    def __init__(self, controller):
        self.controller = controller

        super().__init__()
        self.setWindowTitle("Browser Agent")
        self.setGeometry(100, 100, 720, 640)

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)
        
        top_section = QWidget()
        top_section.setObjectName("topSection")
        top_layout = QVBoxLayout(top_section)
        top_layout.setContentsMargins(2, 2, 2, 2)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setPlaceholderText("There will be text soon...")
        self.result_output.setObjectName("resultOutput")
        self.result_output.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.result_output.setMinimumHeight(256)
        
        top_layout.addWidget(self.result_output)

        center_section = QWidget()
        center_section.setObjectName("centerSection")
        center_section.setMinimumHeight(62)
        center_layout = QHBoxLayout(center_section)
        center_layout.setContentsMargins(2, 2, 12, 2)
        center_layout.setSpacing(12)

        self.api_key_field = QLineEdit()
        self.api_key_field.setObjectName("apiKeyField")
        self.api_key_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.api_key_field.setPlaceholderText("Put Z.AI API key here...")

        check_api_button = QPushButton("Check API-key")
        check_api_button.setObjectName(f"sendButton")
        check_api_button.setMinimumSize(120, 42)
        check_api_button.setMaximumSize(120, 42)
        check_api_button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        check_api_button.clicked.connect(lambda btn=check_api_button: self.add_text_to_result_output(f"Button: {button.text()}"))

        center_layout.addWidget(self.api_key_field)
        center_layout.addWidget(check_api_button)

        bottom_section = QWidget()
        bottom_section.setObjectName("bottomSection")
        bottom_section.setMinimumHeight(116)
        bottom_section.setMaximumHeight(116)
        bottom_layout = QHBoxLayout(bottom_section)
        bottom_layout.setSpacing(12)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        left_column = QWidget()
        left_column.setObjectName("leftColumn")
        left_column_layout = QVBoxLayout(left_column)
        left_column_layout.setContentsMargins(2, 2, 2, 2)
        
        input_buttons_container = QWidget()
        input_buttons_container.setObjectName("inputButtonsContainer")
        input_buttons_layout = QHBoxLayout(input_buttons_container)
        input_buttons_layout.setSpacing(0)
        input_buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Write prompt there...")
        self.query_input.setObjectName("queryInput")
        self.query_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.query_input.setMinimumWidth(200)
        
        buttons_vertical_container = QWidget()
        buttons_vertical_container.setObjectName("buttonsVerticalContainer")
        buttons_vertical_container.setMinimumWidth(48)
        buttons_vertical_layout = QVBoxLayout(buttons_vertical_container)
        buttons_vertical_layout.setSpacing(8)
        buttons_vertical_layout.setContentsMargins(12, 12, 12, 12)
        
        self.send_button = QPushButton()
        self.send_button.setObjectName("sendButton")
        self.send_button.setToolTip("Send prompt")
        self.send_button.clicked.connect(self.on_send_click)
        self.send_button.setFixedSize(40, 40)
        self.send_button.setIcon(QIcon("ui/img/send.svg"))
        self.send_button.setIconSize(QSize(24, 24))

        self.extra_button = QPushButton()
        self.extra_button.setObjectName("extraButton")
        self.extra_button.setToolTip("Secret")
        self.extra_button.clicked.connect(self.on_extra_button_click)
        self.extra_button.setFixedSize(40, 40)
        self.extra_button.setIcon(QIcon("ui/img/microphone.svg"))
        self.extra_button.setIconSize(QSize(24, 24))
        
        buttons_vertical_layout.addWidget(self.send_button)
        buttons_vertical_layout.addWidget(self.extra_button)
        buttons_vertical_layout.addStretch()
        
        input_buttons_layout.addWidget(self.query_input)
        input_buttons_layout.addWidget(buttons_vertical_container)
        
        left_column_layout.addWidget(input_buttons_container)
        
        right_column = QWidget()
        right_column.setObjectName("rightColumn")
        right_column.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        right_column_layout = QVBoxLayout(right_column)
        right_column_layout.setSpacing(0)
        right_column_layout.setContentsMargins(0, 0, 0, 0)
        
        buttons_container = QWidget()
        buttons_container.setObjectName("buttonsGridContainer")
        buttons_grid = QGridLayout(buttons_container)
        buttons_grid.setSpacing(8)
        buttons_grid.setContentsMargins(12, 12, 12, 12)
        
        button_texts = [
            ["Clear", "Stop"],
            ["Save", "Secret"]
        ]
        
        self.buttons = []
        for row in range(2):
            for col in range(2):
                button = QPushButton(button_texts[row][col])
                button.setObjectName(f"sendButton")
                button.setMinimumSize(120, 42)
                button.setMaximumSize(120, 42)
                button.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Expanding
                )
                button.clicked.connect(lambda btn=button: self.add_text_to_result_output(f"Button: {button.text()}"))
                buttons_grid.addWidget(button, row, col)
                self.buttons.append(button)
        
        right_column_layout.addWidget(buttons_container)
        right_column_layout.addStretch()
        
        bottom_layout.addWidget(left_column, 2)
        bottom_layout.addWidget(right_column, 1)
        
        main_layout.addWidget(top_section, 8)
        main_layout.addWidget(center_section, 1)
        main_layout.addWidget(bottom_section, 2)
        
        self.load_styles("style/styles.css")
    
    def load_styles(self, filename):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                
        except Exception as e:
            print(f"Styles error: {e}")
    
    def add_text_to_result_output(self, text):
        self.result_output.append(text)

    # def on_button_click(self, button):
    #     button_text = button.text()
    #     self.add_text_to_result_output(f"Button: {button_text}")
    
    def on_extra_button_click(self):
        self.controller.stop_thread()
    
    def on_send_click(self):
        query = self.query_input.toPlainText()
        self.query_input.clear()
        self.controller.start_prompt_processing_in_thread(query)

    def closeEvent(self, event: QCloseEvent):
        print("SHUTDOWN")
        self.controller.stop_thread()
        
        event.accept()
