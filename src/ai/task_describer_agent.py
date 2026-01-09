import json

from zai import ZaiClient

class TaskDescriberAgent:
    def __init__(self, api_key):
        self.client = ZaiClient(api_key=api_key)
        self.model = "glm-4.6v-flash"
    
    def change_key(self, key):
        self.client = ZaiClient(api_key=key)

    def describe_task(self, messages):
        response = self.client.chat.completions.create(
            model="glm-4.6v-flash",
            messages=messages,
            max_tokens=5000
        )

        choice = response.choices[0]

        if not choice.finish_reason == "stop":
            return False, choice.message.content, "Не удалось уложиться в заданную длину запроса"

        is_success, json_message = self.get_json_from_ai_output(choice.message.content)
        if not is_success:
            return False, choice.message.content, "Не удалось обработать запрос агента"

        usage_info = response.usage
        print(f"Prompt tokens (input): {usage_info.prompt_tokens}")
        print(f"Completion tokens (output): {usage_info.completion_tokens}")
        print(f"Total tokens: {usage_info.total_tokens}")

        return True, json_message, ""

    def get_json_from_ai_output(self, ai_output):
        json_message = {}

        try:
            json_message = json.loads(ai_output)
        except json.decoder.JSONDecodeError as e:
            return False, json_message
        
        is_success = self.check_getting_url_ai_message(json_message)

        return is_success, json_message

    def check_getting_url_ai_message(self, json_message):
        try:
            if not (isinstance(json_message['language'], str) and isinstance(json_message['url'], str) and
                    isinstance(json_message['description'], str) and isinstance(json_message['is_valid'], str)):
                return False
        except (KeyError, TypeError):
            return False
        return True

    def stop_agent(self):
        pass
