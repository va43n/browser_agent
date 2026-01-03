from enviroment.env_handler import EnviromentHandler
from ui.terminal_ui import TerimnalUI

class Controller:
    def __init__(self):
        self.t_ui = TerimnalUI()
        self.env = EnviromentHandler()
        
        is_available, key = self.env.get_api_key()
        if not is_available:
            api_key_user_input = self.t_ui.handle_not_available_api_key()
            self.env.set_api_key_from_ui(api_key_user_input)
        
        self.t_ui.ready_to_start()
        self.handle_prompts()

    def handle_prompts(self):
        is_going = True
        while is_going:
            user_input = self.t_ui.get_prompt_from_user()
            if user_input == "quit":
                is_going = False
            else:
                print(f"Your prompt: {user_input}")

if __name__ == "__main__":
    c = Controller()