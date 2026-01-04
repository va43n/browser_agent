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
        self.page = self.browser.new_page()
    
    def open_url(self, url):
        result = ""
        is_success = True
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            
            html_content = self.page.content()
            title = self.page.title()
            url = self.page.url

            # self.page.screenshot(path="example_screenshot.png")

            print(f"Страница загружена: {title}")
            print(f"URL: {url}")
            print(f"Длина HTML: {len(html_content)} символов")

            result = self.clear_html_and_get_useful_elements(title, url, html_content)

            # self.page.locator("[name='login']").fill("qwerty123456")
            # self.page.type("[name='login']", "hello world", delay=50)
            
        except Exception as e:
            result = "error"
            is_success = False
            print(f"Error: {e}")
        
        return is_success, result
    
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