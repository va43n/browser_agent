import re

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
    
    def get_page_info(self):
        result = ""
        is_success = True

        html_content = self.page.content()
        title = self.page.title()
        url = self.page.url

        print(f"Страница загружена: {title}")
        print(f"URL: {url}")
        print(f"Длина HTML: {len(html_content)} символов")

        result = self.clear_html_and_get_useful_elements(title, url, html_content)
        
        return is_success, result

    def perform_action(self, json_message):
        if json_message['command']['action'] == "click":
            self.click_on_object(json_message['command']['name'])
        elif json_message['command']['action'] == "fill":
            self.fill_input_field(json_message['command']['name'], json_message['command']['text'])

    def click_on_object(self, object_text):
        self.page.click(f"text={object_text}")

    def fill_input_field(self, input_field_name, text):
        self.page.locator(f"[name='{input_field_name}']").fill(f"{text}")

    def clear_html_and_get_useful_elements(self, title, url, html):
        html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html, flags=re.IGNORECASE)

        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)

        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
        if body_match:
            html = body_match.group(1)

        return self.extract_useful_elements(title, url, html)

    def extract_useful_elements(self, title, url, html):
        useful_elements = f"[{url}]\n[{title}]\n"
        
        buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.IGNORECASE | re.DOTALL)
        for i, btn in enumerate(buttons[:10]):
            btn_text = re.sub(r'<[^>]+>', '', btn).strip()[:50]
            if btn_text:
                useful_elements += f"<button> {i + 1} [{btn_text}]\n"
        
        links = re.findall(r'<a[^>]*href=["\'][^"\']*["\'][^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
        for i, link in enumerate(links[:10]):
            link_text = re.sub(r'<[^>]+>', '', link).strip()[:50]
            if link_text:
                useful_elements += f"<a> {i + 1} [{link_text}]\n"
        
        inputs = re.findall(r'<input[^>]*>', html, re.IGNORECASE)
        for i, inp in enumerate(inputs[:10]):
            input_name = re.search(r'name=["\'][^"\']*["\']', inp)
            input_type = re.search(r'type=["\'][^"\']*["\']', inp)
            name = input_name.group(0)[6:-1] if input_name else f"input_{i+1}"
            type_ = input_type.group(0)[6:-1] if input_type else "text"
            
            useful_elements += f"<input> {i + 1} [{type_}] [{name}]\n"
        
        return useful_elements

    def close(self):
        self.browser.close()
        print(f"Browser is closed.")