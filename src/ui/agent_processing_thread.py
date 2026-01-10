from PySide6.QtCore import QThread

class AgentProcessingThread(QThread):    
    def __init__(self, controller, user_input):
        super().__init__()
        self.user_input = user_input
        self.controller = controller
        self.is_running = True
    
    def run(self):
        self.controller.send_prompt(self.user_input, self)
        
    def stop(self):
        self.is_running = False