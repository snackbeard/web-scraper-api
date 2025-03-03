from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api.models.api_driver_options import ApiDriverOptions


class Scraper:
    def __init__(self, webdriver_remote_host: str):
        self._webdriver_remote_host = webdriver_remote_host

    def get(self, driver_options: ApiDriverOptions) -> webdriver.Remote:
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        if driver_options is not None:
            for option in driver_options.options:
                options.add_argument(option)

            options.add_argument(f'--user-agent={driver_options.user_agent}')

        return webdriver.Remote(command_executor=self._webdriver_remote_host, options=options)
