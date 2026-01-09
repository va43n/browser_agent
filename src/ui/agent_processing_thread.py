from PySide6.QtCore import QThread, Signal

class AgentProcessingThread(QThread):
    # progress = Signal(str)
    
    def __init__(self, controller, user_input):
        super().__init__()
        self.user_input = user_input
        self.controller = controller
    
    def run(self):
        self.controller.send_prompt(self.user_input)