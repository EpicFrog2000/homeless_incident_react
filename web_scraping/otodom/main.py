from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('log-level=3')
        options.add_argument("--incognito")
        options.add_argument("--pageLoadStrategy=eager")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-default-apps')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-remote-fonts')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-component-extensions-with-background-pages')
        options.add_argument("--disable-javascript")

        self.bot = webdriver.Chrome(options=options)
        url = 'https://www.otodom.pl/'
        self.bot.get(url)
        self.bot.maximize_window()
    
    def accept_cookies(self):
        button = WebDriverWait(self.bot, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        button.click()

        


if __name__ == "__main__":
    bot = Bot()
    bot.accept_cookies()
    input("xd")