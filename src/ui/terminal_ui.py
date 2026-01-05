class TerimnalUI:
    def __init__(self):
        self.show_start_menu()

    def show_start_menu(self):
        print("Привет! Я - ИИ-агент, и я помогу тебе выполнить различные задачи с браузером.")
    
    def handle_not_available_api_key(self):
        print("ВНИМАНИЕ: Вы не ввели API-ключ для Zhipu AI, поэтому я пока что не смогу ответить на твои запросы. Однако вы можете ввести ключ прямо сейчас: ")
        return input()

    def ready_to_start(self):
        print("API-ключ введен. Можно приступать к работе!")
    
    def get_prompt_from_user(self):
        print("Введи свой запрос, и я попробую его обработать! Для завершения напиши 'quit'.")
        return input()

    def show_message(self, message):
        print(message)
