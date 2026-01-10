from ai.agent_handler import AgentHandler
from environment.env_handler import EnvironmentHandler
from ui.gui_manager import GUI
from ui.agent_processing_thread import AgentProcessingThread

class Controller:
    def __init__(self):
        self.is_api_key_correct = False
        self.env = EnvironmentHandler()

        self.agent_handler = None

        self.thread = None
        self.is_thread_going = False
        
        self.gui = GUI(self)
        self.gui.start_app()

    def start_prompt_processing_in_thread(self, user_input):
        self.gui.check_api_key_and_show_result()
        # self.check_api_key()
        if not self.is_api_key_correct:
            # self.gui.add_text_to_result_output("Your API-key is incorrect! Please change it and press check button")
            return
        self.is_thread_going = True
        self.thread = AgentProcessingThread(self, user_input)
        self.thread.start()

    def stop_thread(self):
        if self.is_thread_going:
            self.thread.stop()
            self.is_thread_going = False

    def send_prompt(self, user_input):
        self.agent_handler.process_new_prompt(user_input, self.gui)
        self.gui.set_initial_state_of_send_button()

    def get_api_key(self):
        is_available, key = self.env.get_api_key()
        return key if is_available else ""

    def check_api_key(self):
        if self.is_api_key_correct:
            return True
        key = self.gui.get_api_key_from_input_field()
        if key == "":
            return False
        if self.agent_handler is None:
            self.agent_handler = AgentHandler(key)

        is_correct = self.agent_handler.check_key(key)

        self.is_api_key_correct = is_correct
        if self.is_api_key_correct:
            self.env.set_api_key(key)

        return self.is_api_key_correct

if __name__ == "__main__":
    c = Controller()
