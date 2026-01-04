from .browser import Browser

class BrowserHandler:
    def __init__(self):
        self.browser = None

    def start_browser(self):
        if self.browser is not None:
            self.browser.close()
            self.browser.start()
        else:
            self.browser = Browser()
    
    def open_url_in_browser(self, url):
        return self.browser.open_url(url)

    def close_browser(self):
        if self.browser is not None:
            # self.browser.save_session("github_session.json")
            self.browser.close()
