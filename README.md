# browser_agent

[Версия на русском языке доступна здесь](README_RUS.md)  
A browser automation app using an AI agent.  
[Installation](#installation)  
[Run](#run)  
[Documentation](#documentation)  
[Information](#information)  

## Installation
After cloning the repository, you need to:  
1. Make sure Python version 3.12 or later is installed:
```bash
python --version
>> Python 3.11.4
```
2. Go to src:
```bash
cd src
ls
>> ai environment ui main.py requirements.txt
```
3. Create and activate venv (one of the options):
```bash
python -m venv venv
./venv/Scripts/activate
```
4. Install all dependencies:
```bash
pip install -r requirements.txt
```

## Run
To run the application you need to:  
1. Activate venv in src (if not already activated):
```bash
./venv/Scripts/activate
```
2. Run the application from src:
```bash
python main.py
```

## Documentation
1. The application has three main fields: the top one is for outputting information from the agent, the middle one is for entering the API key, and the bottom one is for making a request.

2. The application has four buttons: yellow - for checking the API key, green - for sending a request, blue - for saving the JSON report, and red - for clearing the output field.

3. The AI ​​agent runs on the glm-4.6v-flash from [Zhipu AI](https://z.ai/subscribe), so to work with the agent, you need to obtain an API key from the official website. Once obtained, paste the key into the middle field of the application.  
4. To verify the API key, click the yellow button to the right of the middle field. If successful, the yellow button will turn green, and the API key will be saved in the system for future use.

5. If you don't verify the API key manually, it will be automatically verified when sending a request.

6. Send the request by clicking the green button.

7. While the application is running, the agent will periodically send various messages to the top field. Clicking the red button will completely clear this field.

8. Clicking the blue button will save the current session as a JSON report. A session might look like this:
```json
{
    "prompts": [
        [
            ["role": "user", "content": "[prompt...]"]
            ["role": "assistant", "content": "[result...]"]
            ...
        ]
        [
            ["role": "user", "content": "[second prompt...]"]
            ["role": "assistant", "content": "[result...]"]
            ...
        ]
        ...
    ],
    "session_number": [session number]
    "start_time": "HH:MM:SS"
}
``
9. Each session is described by its start time, session number, and a set of "prompts" consisting of lists of responses to user requests. The session is saved in the file "Session_[start_time]_[session_number].json".  
10. When a valid user request is processed, the Chromium browser will be opened, where the AI ​​agent will then attempt to complete the task. A description of each action performed will appear in the top field.  
11. If you click the green button while the request is executing, the AI ​​agent will stop executing the user request shortly.

## Information
1. The glm-4.6v-flash from [Zhipu AI](https://z.ai/subscribe) is used as the model.

2. The official Z.ai SDK is used to access the model.

3. The Playwright library is used for browser automation.  
4. BeautifulSoup is used to extract information from the page. It finds the necessary HTML elements on the page (currently, only "button", "a", and "input" are considered) and defines the attributes needed for analysis.  
5. To perform an action on a browser page, a tool-calling architecture is used: the model is trained to produce JSON output in a specific format, which is then programmatically checked for correctness and processed according to the task.  
6. The Sub-agent architecture pattern is used. The program has three types of tasks for the AI ​​agent: checking the API key for correctness, determining the task and page URL based on user input, and determining the current task based on page content. A separate agent is responsible for each task.  
7. The Security Layer pattern is used. The model is notified that if a task involves a destructive action, it should perform all other actions before it and stop.  
8. The agent description does not include special agent action templates, predefined selectors, or element hints.  
9. Programming language - Python.  
10. GUI library - Pyside6.  