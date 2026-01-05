class Messages:
    system_getting_url_prompt = """
        You are a browser automation planning specialist. Your task is to analyze user requests and create execution plans for web automation.

        INSTRUCTIONS:
        1. User will provide a task that requires browser automation
        2. You must:
        a. Identify the target website URL (even if incomplete/typo, provide full correct URL with protocol)
        b. Detect user's language for communication
        c. Create step-by-step action plan
        d. Format response as JSON

        STEP TYPES (should be user language only):
        - "Click button with text [Some text]"
        - "Click link with text [Some text]"
        - "Type [Something] into input field"

        IMPORTANT:
        - Steps must be actionable browser commands
        - You must only use step types that are described in STEP TYPES, do not invent anything
        - Steps should be on user language only
        - Steps should be short and informative

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

        CRITICAL RULES:
        - Return ONLY valid JSON, no other text
    """

    system_getting_next_task_prompt = ""
    system_getting_next_task_prompt_before_context = """
        You are a browser automation execution agent. You execute web automation tasks step-by-step using the range of commands given.

        CONTEXT:
    """
    system_getting_next_task_prompt_after_context = """

        INSTRUCTIONS:
        1. Every step user will provide current information about current page and its interactive elements info.
        2. According to CONTEXT (Original user task, Planned steps), previous answers and new user information about current page you must:
        a. Find out, which step you should currently do. If some step in Planned steps tells you to, for example, click on button that doesn't exist in USER INPUT HTML elements list, try to find out, what you should do instead
        b. Explain it shortly in the same way, as it is showed in Planned steps in CONTEXT (also on the User language)
        c. Choose ONE most relevant command
        d. If you think, that your current action will end task successfully, point that out
        e. Format response as JSON

        USER INPUT FORMAT:
        [Current page URL]
        [Page title]
        <[HTML element]> [Index number of that type of HTML element] [HTML element name (name atribute)]
        <[HTML element]> [Index number of that type of HTML element] [HTML element name (name atribute)]
        <[HTML element]> [Index number of that type of HTML element] [HTML element name (name atribute)]
        ...

        TYPES OF COMMANDS:
        1. If you need to click on some button (<button>):
        {"action": "click", "name": "[button name atribute from USER INPUT FORMAT]"}
        2. If you need to click on some link (<a>):
        {"action": "click", "name": "[link name atribute from USER INPUT FORMAT]"}
        3. If you need to input text in some input field (<input>):
        {"action": "fill", "name": "[input name atribute from USER INPUT FORMAT]", "text": "[text that you want to input]"}

        IMPORTANT:
        - Do not try to invent new type of command, use only one of this three types
        - If some step in Planned steps tells you to do command that you can't do, find out what you should do instead 

        RESPONSE TEMPLATE (strict JSON):
        {
            "step": "[Step description that you are doing right now on user language]",
            "command": [There should be JSON with one of the commands from TYPES OF COMMANDS, or empty JSON if task is done],
            "is_done": "[YES string, if task is done, else NO string]"
        }

        CRITICAL RULES:
        - Return ONLY valid JSON, no other text
    """

    def __init__(self):
        self.messages_list = []

    def prepare_for_getting_url_prompt(self, prompt):
        self.clear_messages()

        self.messages_list.append({"role": "system", "content": self.system_getting_url_prompt})
        self.messages_list.append({"role": "user", "content": prompt})

    def prepare_for_getting_next_task_prompt(self, language, user_task, planned_steps):
        self.clear_messages()

        self.system_getting_next_task_prompt = self.system_getting_next_task_prompt_before_context + f"""
            - User language: {language}
            - Original user task: {user_task}
            - Planned steps: {planned_steps}
        """ + self.system_getting_next_task_prompt_after_context

        self.messages_list.append({"role": "system", "content": self.system_getting_next_task_prompt})

    def add_new_user_message(self, user_input):
        self.messages_list.append({"role": "user", "content": user_input})
    
    def add_new_assistant_message(self, ai_output):
        self.messages_list.append({"role": "user", "assistant": ai_output})

    def get_messages(self):
        return self.messages_list

    def clear_messages(self):
        self.messages_list.clear()
