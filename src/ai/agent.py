import json

from zai import ZaiClient

from .browser_tasks.browser_handler import BrowserHandler

class Agent:
    planning_prompt = """
        You are a browser automation planning specialist. Your task is to analyze user requests and create execution plans for web automation.

        INSTRUCTIONS:
        1. User will provide a task that requires browser automation
        2. You must:
        a. Identify the target website URL (even if incomplete/typo, provide full correct URL with protocol)
        b. Detect user's language for communication
        c. Create step-by-step action plan (max 10 steps)
        d. Format response as JSON

        STEP FORMAT (English only):
        - "Click button with text [Some text]"
        - "Click link with text [Some text]"
        - "Type [Something] into input field"
        - etc

        RESPONSE TEMPLATE (strict JSON):
        {
            "language": "[detected language code (en/ru/etc)]",
            "url": "[full correct URL with protocol]",
            "opening_message": "Opening [website_name]... (in user's language)",
            "steps": [
                "Step 1 description",
                "Step 2 description",
                ...
            ]
        }

        IMPORTANT:
        - Steps must be actionable browser commands
        - Maximum 10 steps
        - Steps should be on English only
        - Steps should be short and informative
    """

    def __init__(self, api_key):
        self.client = ZaiClient(api_key=api_key)
        self.model = "glm-4.6v-flash"

        # self.b = BrowserHandler()
    
    def process_prompt(self, prompt):
        messages = [
            {"role": "system", "content": self.planning_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model="glm-4.6v-flash",
            messages=messages,
            max_tokens=5000
        )

        print(f"Request ID: {response.id}")
        print(f"Unix timestamp: {response.created}")
        print(f"Used model: {response.model}")
        print(f"Object type: {response.object}")

        print(f"Number of choices: {len(response.choices)}")
        choice = response.choices[0]
        print(f"Finish reason: {choice.finish_reason}")
        print(f"Message role: {choice.message.role}")
        print(f"Message content: {choice.message.content}")

        # message_json = json.loads(choice.message.content)
        # print(f"Message in json: {message_json}")
        # print(f"Some field from json: {message_json['language']=}, {message_json['url']=}, {message_json['opening_message']=}, {message_json['steps']=}")

        usage_info = response.usage
        print(f"Prompt tokens (input): {usage_info.prompt_tokens}")
        print(f"Completion tokens (output): {usage_info.completion_tokens}")
        print(f"Total tokens: {usage_info.total_tokens}")

        # self.b.start_browser()
        # is_success, elements = self.b.open_url_in_browser(prompt)

        # print(f"Is page loaded: {is_success}")
        # print(f"Length of useful elements {len(elements)}")
        # print(f"Elements:\n{elements}")

    def stop_agent(self):
        # self.b.close_browser()
        pass
