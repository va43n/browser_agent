import os

from zai import ZaiClient
from dotenv import load_dotenv

load_dotenv()
client = ZaiClient(api_key=os.getenv("ZAI_API_KEY"))

response = client.chat.completions.create(
    model="glm-4.6v-flash",
    messages=[
        {"role": "user", "content": "Привет, представься кратко."}
    ],
    max_tokens=1000
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

usage_info = response.usage
print(f"Prompt tokens (input): {usage_info.prompt_tokens}")
print(f"Completion tokens (output): {usage_info.completion_tokens}")
print(f"Total tokens: {usage_info.total_tokens}")
