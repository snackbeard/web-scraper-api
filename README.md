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
This API is using **FastAPI**, **Selenium** and **chromedriver** and takes a list of instructions
and calls the corresponding selenium functions to control the chromedriver.
To run it in a Docker Container build an image with the corresponding Dockerfile.
  
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

When running in docker make sure to use **always** specify the following options otherwise it
will not work
~~~python
    options = DriverOptions(
        user_agent='...',
        options=['--headless', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
    )
~~~

---

### Future Improvements
1. support proxies to avoid ip bans
2. more actions and/or more details for an action