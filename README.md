### Goal
This project aims to simplify the webscraping process with Selenium by providing an easy to use client library to access
a self hosted instance of **Selenium Grid**.  

---

Standard usage:
~~~python
import logging
import time

from selenium import webdriver
from selenium.common import TimeoutException, JavascriptException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

chrome_options: Options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

service: Service = Service('/path/to/chromedriver')
driver: webdriver.Chrome = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://my-url.com')

try:
    # accept cookies
    cookie_button = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((
            By.CSS_SELECTOR,
            'button.sc-aXZVg.sc-lcIPJg.fkTzLw.jlhbaU.acceptAll'
        ))
    )
    driver.execute_script('arguments[0].click();', cookie_button)
except TimeoutException as e:
    logging.info('element not present')

try:
    # wait for page to load
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-iwOjIX.cPJSFQ.events-list'))
    )

    time.sleep(1)

    # scroll down a bit
    element_to_scroll = driver.find_element(By.CSS_SELECTOR, 'div.sc-iwOjIX.cPJSFQ.events-list')
    driver.execute_script('arguments[0].scrollIntoView({block: "end"});', element_to_scroll)

    time.sleep(1)

    element_to_scroll = driver.find_element(By.CSS_SELECTOR, 'div.sc-PXPPG.hIImXk')
    driver.execute_script('arguments[0].scrollIntoView({block: "start"});', element_to_scroll)

except TimeoutException | JavascriptException as e:
    logging.info('error')

page_source = driver.page_source
~~~

---

With client library:
~~~python
from client.enums.api_instruction_block_type import ApiInstructionBlockType
from client.enums.api_instruction_content_type import ApiInstructionContentType
from client.enums.api_instruction_element_type import ApiInstructionElementType
from client.enums.api_instruction_identificator_type import ApiInstructionIdentificatorType
from client.models.driver_options import DriverOptions
from client.webscraper_instruction_builder import WebScraperInstructionBuilder

options = DriverOptions(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', options=[
    '--headless',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage'
])

page_source = WebScraperInstructionBuilder(url='api-url', 
                                           api_key='api-key')\
                .wait_for(seconds=10, 
                          wait_for=ApiInstructionElementType.ELEMENT_CLICKALBE,
                          by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                          element_id='button.sc-aXZVg.sc-lcIPJg.fkTzLw.jlhbaU.acceptAll',
                          ignore_error=True)\
                .wait_for(seconds=10,
                            wait_for=ApiInstructionElementType.ELEMENT_PRESENCE,
                            by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                            element_id='div.sc-iwOjIX.cPJSFQ.events-list')\
                .wait(seconds=1)\
                .scroll(ApiInstructionBlockType.END)\
                .wait(seconds=1)\
                .find(by=ApiInstructionIdentificatorType.CSS_SELECTOR, element_id='div.sc-PXPPG.hIImXk')\
                .scroll(ApiInstructionBlockType.START)\
                .get(page_url='page-to-scrape-url', options=options, content=ApiInstructionContentType.PAGE_SOURCE)
~~~

### Client Library
The client library makes it easy to access the API by providing a builder class.
**Example:**
~~~python
    options = DriverOptions(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        options=['--headless', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
    )

    page_source = WebScraperBuilder(
                        url='https://my-domain.com',
                        api_key='c1f24ee0-1a77-4719-a33b-408069dfc15f')
                    .wait_for(seconds=5,
                          by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                          wait_for=ApiInstructionElementType.ELEMENT_CLICKALBE,
                          element_id='button.sc-aXZVg.sc-lcIPJg.bjommA.jlhbaU.acceptAll',
                          ignore_error=True)
                    .click(ignore_error=True)
                    .wait_for(seconds=10,
                          by=ApiInstructionIdentificatorType.CSS_SELECTOR,
                          wait_for=ApiInstructionElementType.ELEMENT_PRESENCE,
                          element_id='div.category-event-items')
                    .scroll(block=ApiInstructionBlockType.END)
                    .get(page_url='https://www.page-to-scrape.com', options=options)
~~~
In the first _.wait_ instruction a cookie dialog overlaps with the actual content we want
to scrape. So to accept it we have to wait for the _.acceptAll_ button to be clickable and
then click it. Cookies won't appear again after accepting them once so if we scrape the site
again an error would appear. So _ignore_error_ is set to true in both instructions. Then
we wait for an list to be present and scroll to the end of it to load all its content.

The following actions are currently supported
- **wait** - simply waits
    - _seconds_ seconds to wait
- **wait_for** - wait for an element
    - _seconds_ - seconds to wait
    - _by_ - find it either by css selector or by element_id
    - _wait_for_ - wait until the element is either present or clickable
    - _element_id_ - id/selector of the element
    - _ignore_error_ - if an element was not found ignore it and continue with the next instruction
- **find** - find and element
    - _by_ - find it either by css selector or by element id
    - _element_id_ - id/selector of the element
    - _ignore_error_ - ...
- **click** - click an element after finding it or waiting for it
    - _ignore_error_ - ...
- **scroll** - scroll to an element after finding it or waiting for it
    - _block_ - scroll to either end or start
    - _ignore_error - ...
- **get**
    - _page_url_ - webpage to scrape
    - _content_ - page_source (html) or xhr (json)
    - _xhr_name_ - document name (has to be provided if content is xhr)
    - _options_ - chromedriver options

> These instructions should be able to handle most use-cases

---

### API
This API is using **FastAPI** and **Selenium Grid** and takes a list of instructions
and calls the corresponding selenium functions to control the browser. By default
there is no authentication with Selenium Grid so the API provides a simple check for an api-key. Only the API
is exposed, Selenium Grid itself is not.

Docker Compose
~~~yaml
version: "3.5"

services:
  webscraper-api:
    image: webscraper-api
    container_name: webscraper-api
    environment:
      HOST: 0.0.0.0
      PORT: 8081
      X-API-KEY: c1f24ee0-1a77-4719-a33b-408069dfc15f
      LOG_LEVEL: INFO
      WEBDRIVER_REMOTE_HOST: http://selenium-chrome:4444/wd/hub
    ports:
      - "8081:8081"
    networks:
      - scraping-network
    depends_on:
      - selenium-chrome

  selenium-chrome:
    image: selenium/standalone-chrome
    container_name: selenium-chrome
    shm_size: 2g
    networks:
      - scraping-network
    # ports:
      # - "4444:4444"
      # - "7900:7900"

networks:
  scraping-network:
    driver: bridge

~~~

The above configuration only provides one node. To deploy multiple nodes check the Selenium docs: https://github.com/SeleniumHQ/docker-selenium

---

### Future Improvements
1. support proxies to avoid ip bans
2. more actions and/or more details for an action