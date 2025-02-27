from bs4 import BeautifulSoup

from client.enums.api_instruction_block_type import ApiInstructionBlockType
from client.enums.api_instruction_element_type import ApiInstructionElementType
from client.enums.api_instruction_identificator_type import ApiInstructionIdentificatorType
from client.models.driver_options import DriverOptions
from client.webscraper_builder import WebScraperBuilder

def main():
    options = DriverOptions(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        options=['--headless', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
    )

    page_source = WebScraperBuilder(
                        url='https://my-domain.com',
                        api_key='c1f24ee0-1a77-4719-a33b-408069dfc15f')\
                    .wait(seconds=5,
                          by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                          wait_for=ApiInstructionElementType.ELEMENT_CLICKALBE,
                          element_id='button.sc-aXZVg.sc-lcIPJg.bjommA.jlhbaU.acceptAll',
                          ignore_error=True)\
                    .click(ignore_error=True)\
                    .wait(seconds=10,
                          by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                          wait_for=ApiInstructionElementType.ELEMENT_PRESENCE,
                          element_id='div.category-event-items')\
                    .scroll(block=ApiInstructionBlockType.END) \
                    .get(page_url='https://page-to-scrape.com', options=options)
    print()

if __name__ == '__main__':
    main()
