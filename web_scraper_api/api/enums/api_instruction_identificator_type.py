from enum import Enum
from selenium.webdriver.common.by import By

class ApiInstructionIdentificatorType(Enum):
    CSS_SELECTOR = 'css_selector'
    ID = 'id'

    @property
    def webdriver_value(self):
        webdriver_values = {
            'css_selector': By.CSS_SELECTOR,
            'id': By.ID
        }
        return webdriver_values[self.value]