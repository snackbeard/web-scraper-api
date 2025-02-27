from enum import Enum
from selenium.webdriver.support import expected_conditions


class ApiInstructionElementType(Enum):
    ELEMENT_PRESENCE = 'element_presence'
    ELEMENT_CLICKALBE = 'element_clickable'

    @property
    def webdriver_value(self):
        webdriver_values = {
            'element_presence': expected_conditions.presence_of_element_located,
            'element_clickable': expected_conditions.element_to_be_clickable
        }
        return webdriver_values[self.value]
