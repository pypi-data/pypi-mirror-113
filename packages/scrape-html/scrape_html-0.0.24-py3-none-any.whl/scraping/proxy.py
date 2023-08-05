from selenium.webdriver.chrome.options import Options

class Proxy:
    #Config
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable a input error
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--incognito')
    options.add_argument('--disable-infobars')

    def __init__(self, headless: bool, proxy: str) -> None:
        """
            PROXY = "159.203.12.49:8888" # IP:PORT or HOST:PORT
        """
        if headless:
            self.options.add_argument('--headless')
        if proxy:
            print(f'Using proxy: {proxy}')
            self.options.add_argument('--proxy-server=%s' % proxy)