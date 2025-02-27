from selenium.common.exceptions import TimeoutException, JavascriptException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from api.enums.api_instruction_action_type import ApiInstructionActionType
from api.models.api_instruction import ApiInstruction
from api.models.api_instruction_find import ApiInstructionFind
from api.models.api_instruction_scroll import ApiInstructionScroll
from api.models.api_instruction_wait import ApiInstructionWait
from util.exceptions import ScrapeException


class ApiInstructionReader:
    def execute_instruction(self, instruction: ApiInstruction, driver: WebDriver, element: object, instruction_index: int):
        # WAIT
        if instruction.action_type == ApiInstructionActionType.WAIT:
            value: ApiInstructionWait = ApiInstructionWait.model_validate(instruction.action_value)
            try:
                return WebDriverWait(driver, value.seconds).until(
                    value.wait_for.webdriver_value((value.by.webdriver_value, value.id))
                )
            except TimeoutException as e:
                if not instruction.action_ignore_error:
                    raise ScrapeException(f'Timeout while waiting for {value.id}')

        # FIND
        elif instruction.action_type == ApiInstructionActionType.FIND:
            value: ApiInstructionFind = ApiInstructionFind.model_validate(instruction.action_value)
            try:
                return driver.find_element(value.by.webdriver_value, value.id)
            except TimeoutException as e:
                if not instruction.action_ignore_error:
                    raise ScrapeException(f'Could not find {value.id}')

        # CLICK
        elif instruction.action_type == ApiInstructionActionType.CLICK:
            try:
                driver.execute_script('arguments[0].click();', element)
            except JavascriptException as e:
                if not instruction.action_ignore_error:
                    raise ScrapeException(f'Could not click the element from the previous instruction: {str(instruction_index - 1)}')

        # SCROLL
        elif instruction.action_type == ApiInstructionActionType.SCROLL:
            value: ApiInstructionScroll = ApiInstructionScroll.model_validate(instruction.action_value)
            driver.execute_script('arguments[0].scrollIntoView({block: "' + value.block.value + '"});', element)
        else:
            raise ScrapeException(f'Unknown action type {instruction.action_type}')