from ai.agent_handler import AgentHandler
from environment.env_handler import EnvironmentHandler
from ui.gui_manager import GUI
from ui.agent_processing_thread import AgentProcessingThread

class Controller:
    def __init__(self):
        self.env = EnvironmentHandler()
        self.agent_handler = None
        
        self.gui = GUI(self)
        self.gui.start_app()

    def start_prompt_processing_in_thread(self, user_input):
        self.thread = AgentProcessingThread(self, user_input)
        # self.thread.progress.connect(self.update_progress)
        self.thread.start()

    def send_prompt(self, user_input):
        if user_input == "":
            return
        self.check_key()

        self.gui.add_text_to_result_output(f"Your prompt: {user_input}")
        self.agent_handler.process_new_prompt(user_input, self.gui)

    def check_key(self):
        is_available, key = self.env.get_api_key()
        if is_available:
            self.gui.add_text_to_result_output("KEY AVAILABLE")
            if self.agent_handler is None:
                self.agent_handler = AgentHandler(key)
            else:
                # self.agent_handler.change_key(key)
                pass
        else:
            self.gui.add_text_to_result_output("KEY UNAVAILABLE")

if __name__ == "__main__":
    c = Controller()
