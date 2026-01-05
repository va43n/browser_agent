import os

from dotenv import load_dotenv, set_key, find_dotenv

class EnvironmentHandler:
    api_key_name = "ZAI_API_KEY"

    def __init__(self):
        self.dotenv_path = find_dotenv()
        if not self.dotenv_path:
            with open('.env', 'w') as f:
                pass
            self.dotenv_path = find_dotenv()
        load_dotenv(self.dotenv_path)

        self.get_api_key_from_env()
    
    def get_api_key_from_env(self):
        self.api_key = os.getenv(self.api_key_name)
        self.is_api_key_available = self.api_key is not None

    def set_api_key_from_ui(self, key):
        set_key(self.dotenv_path, self.api_key_name, key)
        self.get_api_key_from_env()

    def get_api_key(self):
        return self.is_api_key_available, self.api_key
