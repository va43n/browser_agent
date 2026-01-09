from zai import ZaiClient
from zai.core._errors import APIAuthenticationError

class APICheckerAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "glm-4.6v-flash"
    
    def change_key(self, key):
        self.api_key=key

    def check_api_key(self, messages):
        self.client = ZaiClient(api_key=self.api_key)
        try:
            response = self.client.chat.completions.create(
                model="glm-4.6v-flash",
                messages=messages,
                max_tokens=1,
                temperature=0
            )
        except APIAuthenticationError:
            return False

        choice = response.choices[0]

        print(choice.finish_reason, choice.message.content)

        usage_info = response.usage
        print(f"Prompt tokens (input): {usage_info.prompt_tokens}")
        print(f"Completion tokens (output): {usage_info.completion_tokens}")
        print(f"Total tokens: {usage_info.total_tokens}")

        return True