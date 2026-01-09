from PySide6.QtCore import QThread

class AgentProcessingThread(QThread):    
    def __init__(self, controller, user_input):
        super().__init__()
        self.user_input = user_input
        self.controller = controller
    
    def run(self):
        self.controller.send_prompt(self.user_input)
        
    def stop(self):
        self.requestInterruption()
        self.quit()
        self.wait(2000)