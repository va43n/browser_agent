import sys

from PySide6.QtWidgets import (QApplication)
from PySide6.QtGui import QFont

from .pyside6_ui import MainWindow

class GUI:
    def __init__(self, controller):
        self.controller = controller

    def start_app(self):
        self.app = QApplication(sys.argv)
    
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        
        self.window = MainWindow(self.controller)
        self.window.show()
        sys.exit(self.app.exec())
    
    def add_text_to_result_output(self, text):
        self.window.add_text_to_result_output(text)
