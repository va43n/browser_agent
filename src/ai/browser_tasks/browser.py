import json

from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright

class Browser:
    def __init__(self):
        self.browser = None
        self.page = None

        self.start()
    
    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
    
    def open_url(self, url):
        try:
            self.page = self.browser.new_page()
            self.page.goto(url, wait_until="domcontentloaded")

            # self.page.screenshot(path="example_screenshot.png")
        except Exception as e:
            print(f"Error: {e}")
            return False
        
        return True
    
    def perform_action(self, json_message):
        if json_message['command']['tag'] == "button":
            self.handle_button_action(json_message['command'])
        elif json_message['command']['tag'] == "a":
            self.handle_link_action(json_message['command'])
        elif json_message['command']['tag'] == "input":
            self.handle_input_action(json_message['command'])
        self.page.wait_for_load_state('domcontentloaded')

    def handle_button_action(self, json_command):
        if json_command['action'] == 'click':
            attr = json_command['attr']
            attr_text = json_command['attr_text']
            if attr == 'text':
                self.page.get_by_role("button", name=attr_text).nth(0).click()
            else:
                self.page.locator(f'button[{attr}="{attr_text}"]').nth(0).click()
    
    def handle_link_action(self, json_command):
        if json_command['action'] == 'click':
            attr = json_command['attr']
            attr_text = json_command['attr_text']
            if attr == 'text':
                self.page.get_by_role("link", name=attr_text).nth(0).click()
            else:
                self.page.locator(f'a[{attr}="{attr_text}"]').nth(0).click()

    def handle_input_action(self, json_command):
        if json_command['action'] == 'type':
            attr = json_command['attr']
            attr_text = json_command['attr_text']
            text = json_command['text']
            if attr == 'text':
                self.page.get_by_role("textbox", name=attr_text).nth(0).type(text, delay=100)
            else:
                self.page.locator(f'input[{attr}="{attr_text}"]').nth(0).type(text, delay=100)

    def get_page_info(self):
        result = ""
        is_success = True

        html_content = self.page.content()
        title = self.page.title()
        url = self.page.url

        print(f"Страница загружена: {title}")
        print(f"URL: {url}")
        print(f"Длина HTML: {len(html_content)} символов")

        result = self.extract_useful_elements(title, url, html_content)
        
        return is_success, result

    def extract_useful_elements(self, title, url, html):
        soup = BeautifulSoup(html, 'html.parser')

        elements_string = f"[{url}]\n[{title}]\n"
        i = 0
        elements_length = 50

        for elem in soup.find_all(['input', 'button', 'a']):
            attrs = {}
            attrs['tag'] = elem.name

            elem_text = elem.get_text(strip=True)[:40]
            if elem_text:
                attrs['text'] = elem_text

            for attr in ['name', 'id', 'placeholder', 'title', 'class', 'data-qa']:
                value = elem.get(attr)
                if value:
                    attrs[attr] = value

            print(attrs)
            json_str = f"{i + 1}. " + json.dumps(attrs, ensure_ascii=False) + "\n"
            elements_string += json_str
            i += 1
            
            if i >= elements_length:
                break
        
        return elements_string

    def close(self):
        self.browser.close()
        print(f"Browser is closed.")