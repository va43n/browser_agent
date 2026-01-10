import sys

from PySide6.QtWidgets import (QApplication)
from PySide6.QtGui import QFont

from .session_saver import SessionSaver
from .pyside6_ui import MainWindow

class GUI:
    def __init__(self, controller):
        self.controller = controller
        self.session = SessionSaver()

    def start_app(self):
        self.app = QApplication(sys.argv)
    
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        
        self.window = MainWindow(self.controller, self.session)
        self.window.show()
        sys.exit(self.app.exec())
    
    def add_text_to_result_output(self, text):
        self.window.add_text_to_result_output(text)
    
    def check_api_key_and_show_result(self):
        self.window.check_api_key()

    def get_api_key_from_input_field(self):
        return self.window.api_key_field.text()
    
    def set_initial_state_of_send_button(self):
        self.window.set_initial_state_of_send_button()
