import json

from zai import ZaiClient

from .browser_tasks.browser_handler import BrowserHandler

class BrowserScrollerAgent:
    def __init__(self, api_key):
        self.client = ZaiClient(api_key=api_key)
        self.model = "glm-4.6v-flash"

        self.browser_handler = BrowserHandler()
    
    def open_browser(self, url):
        self.browser_handler.start_browser()

        return self.browser_handler.open_url_in_browser(url)

    def get_page_info(self):
        return self.browser_handler.get_page_info()

    def do_next_browser_action(self, messages):
        print(f"is this empty?: {messages[1]}")
        response = self.client.chat.completions.create(
            model="glm-4.6v-flash",
            messages=messages,
            max_tokens=2000
        )

        choice = response.choices[0]

        if not choice.finish_reason == "stop":
            return False, {}, "Не удалось уложиться в заданную длину запроса"

        is_success, json_message = self.get_json_from_ai_output(choice.message.content)
        if not is_success:
            return False, {}, "Не удалось обработать запрос агента"

        usage_info = response.usage
        print(f"Prompt tokens (input): {usage_info.prompt_tokens}")
        print(f"Completion tokens (output): {usage_info.completion_tokens}")
        print(f"Total tokens: {usage_info.total_tokens}")

        print(f"Going to do action: {json_message['step']}")
        self.browser_handler.perform_action(json_message)

        return True, choice.message.content, ""

    def get_json_from_ai_output(self, ai_output, type):
        json_message = {}

        try:
            json_message = json.loads(ai_output)
        except json.decoder.JSONDecodeError as e:
            return False, json_message
        
        is_success = self.check_getting_next_task_ai_message(json_message)

        return is_success, json_message

    def check_getting_next_task_ai_message(self, json_message):
        try:
            if not (isinstance(json_message['step'], str) and isinstance(json_message['command'], object) and
                    isinstance(json_message['is_done'], str)):
                return False
            if not json_message['command'] == {}:
                if not (isinstance(json_message['command']['action'], str) and json_message['command']['action'] in ("click", "fill") and
                        isinstance(json_message['command']['name'], str)):
                    return False
                if (json_message['command']['action'] == "fill" and not isinstance(json_message['command']['text'], str)):
                    return False
        except (KeyError, TypeError):
            return False
        return True

    def stop_agent(self):
        self.browser_handler.close_browser()
        pass