from datetime import datetime
import json

class SessionSaver:
    def __init__(self):
        self.session_time = datetime.now().strftime("%H-%M-%S")
        self.session_counter = 1
        self.session = {"prompts": [],
                        "session_number": self.session_counter,
                        "start_time": self.session_time}
        self.current_prompt = -1

    def create_prompt(self):
        # print("PROMPT CREATED")
        self.current_prompt += 1
        self.session['prompts'].append([])

    def append_message(self, role, content):
        # print("MESSAGE APPENDED")
        if self.current_prompt < 0:
            self.create_prompt()
        cur_time = datetime.now().strftime("%H-%M-%S")
        self.session['prompts'][self.current_prompt].append({"role": role, "content": content, "time": cur_time})
        return cur_time

    def clear_session(self):
        # print("SESSION CLEAREd")
        self.session['prompts'].clear()
        self.current_prompt = -1

    def save_session(self):
        # print("TRY TO SAVE")
        if len(self.session['prompts']) == 0:
            # print("CANT")
            return
        self.session['session_number'] = self.session_counter
        session_name = f"sessions/Session_{self.session_time}_{self.session_counter}.json"
        with open(file=session_name, mode="w") as json_file:
            json.dump(self.session, json_file, indent=4)

        self.session_counter += 1
