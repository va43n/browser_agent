from .browser_scroller_agent import BrowserScrollerAgent
from .messages import Messages
from .task_describer_agent import TaskDescriberAgent

class AgentHandler:
    def __init__(self, api_key):
        self.task_describer = TaskDescriberAgent(api_key)
        self.browser_scroller = BrowserScrollerAgent(api_key)

        self.m = Messages()
    
    def process_new_prompt(self, prompt):
        self.m.prepare_for_getting_url_prompt(prompt)

        is_success, json_description, error_message = self.task_describer.describe_task(self.m.get_messages())
        if not is_success:
            print(error_message, json_description)
            return False
        if json_description['is_valid'] == "NO":
            print("Промпт не имеет смысла")
            return False
        
        print(f"{json_description['description']=}")
        
        self.m.prepare_for_getting_next_task_prompt(json_description['language'], json_description['description'])

        self.browser_scroller.open_browser(json_description['url'])
        
        self.perform_task()

        return True
    
    def perform_task(self):
        is_complete = False
        action_index = 0
        while not is_complete and action_index < 5:
            is_success, page_info = self.browser_scroller.get_page_info()
            if not is_success:
                print("Не получилось получить данные браузера")
                break
            self.m.add_new_user_message(page_info)

            is_success, response, error = self.browser_scroller.do_next_browser_action(self.m.get_messages())
            if not is_success:
                print(error)
                break
            self.m.remove_last_message()
            self.m.add_new_assistant_message(response)

            print(self.m)

            action_index += 1

    def stop_agents(self):
        self.task_describer.stop_agent()
        self.browser_scroller.stop_agent()