from .api_checker_agent import APICheckerAgent
from .browser_scroller_agent import BrowserScrollerAgent
from .messages import Messages
from .task_describer_agent import TaskDescriberAgent

class AgentHandler:
    def __init__(self, api_key):
        self.is_api_key_correct = False

        self.api_checker = APICheckerAgent(api_key)
        self.task_describer = None
        self.browser_scroller = None

        self.m = Messages()
    
    def change_key(self, key):
        if self.api_checker is not None:
            self.api_checker.change_key(key)
        if self.browser_scroller is not None:
            self.browser_scroller.change_key(key)
        if self.task_describer is not None:
            self.task_describer.change_key(key)

    def check_key(self, key):
        if self.is_api_key_correct:
            return True
        self.api_checker.change_key(key)
        is_key = self.api_checker.check_api_key(self.m.get_checking_api_messages())
        
        if is_key and (self.task_describer is None or self.browser_scroller is None):
            self.task_describer = TaskDescriberAgent(key)
            self.browser_scroller = BrowserScrollerAgent(key)
        
        return is_key

    def process_new_prompt(self, prompt, gui):
        self.m.prepare_for_getting_url_prompt(prompt)

        gui.add_text_to_result_output("Trying to understand your prompt...")
        is_success, json_description, error_message = self.task_describer.describe_task(self.m.get_messages())
        if not is_success:
            gui.add_text_to_result_output(error_message, json_description)
            return False
        if json_description['is_valid'] == "NO":
            gui.add_text_to_result_output("I'm sorry, but I think, that this prompt makes no sense. Please try again with a different prompt.")
            return False
        
        gui.add_text_to_result_output(f"I think, that you wanted to say '{json_description['description']}'. I will try to do my best with this task!")
        
        self.m.prepare_for_getting_next_task_prompt(json_description['language'], json_description['description'])

        self.browser_scroller.open_browser(json_description['url'])
        
        self.perform_task(gui)

        return True
    
    def perform_task(self, gui):
        max_actions_for_one_task = 10

        is_complete = False
        action_index = 0
        while not is_complete and action_index < max_actions_for_one_task:
            gui.add_text_to_result_output("Right now I am looking for something useful on this page")
            is_success, page_info = self.browser_scroller.get_page_info()
            if not is_success:
                print("Can't get browser info")
                break
            self.m.add_new_user_message(page_info)

            gui.add_text_to_result_output("I found some HTML elements. Trying to figure out what to do with this...")
            is_success, response, error, is_done = self.browser_scroller.do_next_browser_action(self.m.get_messages(), gui)
            if not is_success:
                print(error)
                break
            if is_done == "YES":
                is_complete = True
                continue
            self.m.remove_last_message()
            self.m.add_new_assistant_message(response)

            print(self.m)

            action_index += 1

    def stop_agents(self):
        self.task_describer.stop_agent()
        self.browser_scroller.stop_agent()