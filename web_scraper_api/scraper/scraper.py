from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from api.models.api_driver_options import ApiDriverOptions


class Scraper:
    def __init__(self, chromedriver_path: str):
        self._chromedriver_path: str = chromedriver_path

    def get(self, driver_options: ApiDriverOptions):
        chrome_options = Options()
        if driver_options is not None:
            for option in driver_options.options:
                chrome_options.add_argument(option)

            chrome_options.add_argument(f'--user-agent={driver_options.user_agent}')

        service = Service(self._chromedriver_path)
        return webdriver.Chrome(service=service, options=chrome_options)
