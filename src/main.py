from ai.agent_handler import AgentHandler
from environment.env_handler import EnvironmentHandler
from ui.pyside6_ui import GUI
# from ui.terminal_ui import TerimnalUI

class Controller:
    def __init__(self):
        # self.t_ui = TerimnalUI()
        self.gui = GUI()
        self.env = EnvironmentHandler()
        
        is_available, key = self.env.get_api_key()
        if is_available:
            self.gui.add_text_to_result_output("KEY IS AVAILABLE")
            print("OK")
        else:
            self.gui.add_text_to_result_output("KEY IS AVAILABLE")
            # api_key_user_input = self.t_ui.handle_not_available_api_key()
            # self.env.set_api_key_from_ui(api_key_user_input)
        # is_available, key = self.env.get_api_key()
        
        self.agent_handler = AgentHandler(key)

        # self.handle_prompts()

    def handle_prompts(self):
        is_going = True
        while is_going:
            # user_input = self.t_ui.get_prompt_from_user()
            user_input = ""
            if user_input == "quit":
                is_going = False
                self.agent_handler.stop_agents()
            else:
                self.t_ui.show_message(f"Your prompt: {user_input}")
                self.agent_handler.process_new_prompt(user_input)

if __name__ == "__main__":
    c = Controller()
