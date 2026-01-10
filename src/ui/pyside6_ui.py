import os

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QTextEdit,
                               QSizePolicy, QStyle, QLineEdit)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QCloseEvent, QKeyEvent

class MainWindow(QMainWindow):
    def __init__(self, controller, session):
        self.controller = controller
        self.session = session

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
        center_section.setMaximumHeight(62)
        center_layout = QHBoxLayout(center_section)
        center_layout.setContentsMargins(2, 2, 12, 2)
        center_layout.setSpacing(12)

        self.api_key_field = QLineEdit()
        self.api_key_field.setObjectName("apiKeyField")
        self.api_key_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.api_key_field.setEchoMode(QLineEdit.Password)
        self.api_key_field.setPlaceholderText("Put Z.AI API key here...")

        self.set_api_key()

        self.check_api_button = QPushButton()
        self.check_api_button.setObjectName("checkButton")
        self.check_api_button.setToolTip("Check API-key")
        self.check_api_button.setFixedSize(40, 40)
        self.check_api_button.clicked.connect(self.check_api_key)
        self.check_api_button.setIcon(QIcon("ui/img/question_mark.svg"))
        self.check_api_button.setIconSize(QSize(24, 24))

        center_layout.addWidget(self.api_key_field)
        center_layout.addWidget(self.check_api_button)

        bottom_section = QWidget()
        bottom_section.setObjectName("bottomSection")
        bottom_section.setMinimumHeight(68)
        bottom_section.setMaximumHeight(68)
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
        
        buttons_horizontal_container = QWidget()
        buttons_horizontal_container.setObjectName("buttonsHorizontalContainer")
        buttons_horizontal_container.setMinimumWidth(160)
        buttons_horizontal_container.setMaximumWidth(160)
        buttons_horizontal_layout = QHBoxLayout(buttons_horizontal_container)
        buttons_horizontal_layout.setSpacing(8)
        buttons_horizontal_layout.setContentsMargins(12, 12, 12, 12)
        
        self.send_button = QPushButton()
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.on_send_click)
        self.send_button.setFixedSize(40, 40)
        self.set_initial_state_of_send_button()

        self.save_button = QPushButton()
        self.save_button.setObjectName("saveButton")
        self.save_button.setToolTip("Save session")
        self.save_button.clicked.connect(self.on_save_button_click)
        self.save_button.setFixedSize(40, 40)
        self.save_button.setIcon(QIcon("ui/img/save.svg"))
        self.save_button.setIconSize(QSize(24, 24))

        self.clear_button = QPushButton()
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setToolTip("Clear agent output")
        self.clear_button.clicked.connect(self.on_clear_button_click)
        self.clear_button.setFixedSize(40, 40)
        self.clear_button.setIcon(QIcon("ui/img/bin.svg"))
        self.clear_button.setIconSize(QSize(24, 24))
        
        buttons_horizontal_layout.addWidget(self.send_button)
        buttons_horizontal_layout.addWidget(self.save_button)
        buttons_horizontal_layout.addWidget(self.clear_button)
        buttons_horizontal_layout.addStretch()
        
        input_buttons_layout.addWidget(self.query_input)
        input_buttons_layout.addWidget(buttons_horizontal_container)
        
        left_column_layout.addWidget(input_buttons_container)
        
        bottom_layout.addWidget(left_column, 1)
        
        main_layout.addWidget(top_section, 8)
        main_layout.addWidget(center_section, 1)
        main_layout.addWidget(bottom_section, 1)
        
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
    
    def get_api_key_from_input_field(self):
        return self.api_key_field.text()

    def check_api_key(self):
        text = self.get_api_key_from_input_field()
        if text == "":
            return
        
        self.add_text_to_result_output("Trying to check your API-key...")
        is_correct = self.controller.check_api_key()
        if is_correct:
            self.api_key_field.setEnabled(False)

            self.check_api_button.setToolTip("API-key is correct")
            self.check_api_button.setObjectName("sendButton")
            self.check_api_button.style().unpolish(self.check_api_button)
            self.check_api_button.style().polish(self.check_api_button)
            self.check_api_button.update()
            self.check_api_button.setIcon(QIcon("ui/img/check.svg"))
            self.check_api_button.setIconSize(QSize(24, 24))
            self.check_api_button.setEnabled(False)

            self.add_text_to_result_output("Your API-key is correct")
        else:
            self.add_text_to_result_output("Your API-key is incorrect! Please change it and press check button")

    def set_api_key(self):
        key = self.controller.get_api_key()
        self.api_key_field.setText(key)

    def add_text_to_result_output(self, text):
        current_time_string = self.session.append_message("assistant", text)
        self.result_output.append(f"[{current_time_string}] 🤖: {text}")
    
    def on_save_button_click(self):
        print("SAVE")
        # self.controller.stop_thread()
        self.session.save_session()
    
    def on_clear_button_click(self):
        self.result_output.clear()
        self.session.clear_session()
    
    def on_send_click(self):
        print("SEND")
        query = self.query_input.toPlainText()
        if query == "":
            return
        
        self.session.create_prompt()
        self.session.append_message("user", query)

        self.send_button.setIcon(QIcon("ui/img/stop.svg"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setToolTip("Stop")
        
        self.add_text_to_result_output(f"Start working with prompt '{query}'")
        self.query_input.clear()
        self.controller.start_prompt_processing_in_thread(query)

    def set_initial_state_of_send_button(self):
        self.send_button.setIcon(QIcon("ui/img/send.svg"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setToolTip("Send prompt")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return and not event.modifiers():
            self.on_send_click()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):
        print("SHUTDOWN")
        self.controller.stop_thread()
        
        event.accept()
