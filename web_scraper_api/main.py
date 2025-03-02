import json
import logging
import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from selenium.common import WebDriverException
from selenium import webdriver

from api.api_instruction_reader import ApiInstructionReader
from api.enums.api_instruction_content_type import ApiInstructionContentType
from models.query import Query
from scraper.scraper import Scraper
from util.configuration import Configuration
from util.exceptions import ScrapeException

load_dotenv()
configuration: Configuration = Configuration()

logging.basicConfig(level=logging.getLevelName(configuration.log_level), format='%(asctime)s - %(levelname)s - %(message)s')

app: FastAPI = FastAPI()

@app.post(path='/api/v1/instructions', status_code=200, response_class=JSONResponse)
def scrape_webpage(query: Query, request: Request) -> JSONResponse:
    if 'x-api-key' not in request.headers.keys() or request.headers.get('x-api-key') != configuration.api_key:
        raise HTTPException(status_code=403)

    if query.content_type == ApiInstructionContentType.XHR and query.xhr_name is None:
        raise HTTPException(status_code=400, detail='With XHR a document name has to be specified')

    driver: webdriver.Chrome = Scraper(webdriver_remote_host=configuration.webdriver_remote_host).get(driver_options=query.options)
    driver.get(url=query.url)

    last_element = None

    try:
        for idx, instruction in enumerate(query.instructions):
            last_element = ApiInstructionReader().execute_instruction(instruction=instruction, driver=driver,
                                                                      element=last_element, instruction_index=idx)

        if query.content_type == ApiInstructionContentType.PAGE_SOURCE:
            return JSONResponse(content={
                'scraped_content': driver.page_source
            })

        if query.content_type == ApiInstructionContentType.XHR:
            logs = driver.get_log('performance')

            logging.info(f'found {len(logs)} logs')

            for log in logs:
                try:
                    log_json = json.loads(log['message'])
                    if 'Network.responseReceived' in log_json['message']['method']:
                        log_url = log_json['message']['params']['response']['url']
                        logging.info(log_url)

                        if query.xhr_name in log_url:
                            request_id = log_json['message']['params']['requestId']

                            logging.info(f'found {query.xhr_name}, request_id: {request_id}')

                            response_body = _get_response_body(driver, request_id)
                            return JSONResponse(content={
                                'scraped_content': json.loads(response_body['body'])
                            })
                except KeyError as ke:
                    pass
                except ScrapeException as se:
                    raise HTTPException(status_code=400, detail='No resource with given identifier found')

            raise HTTPException(status_code=400, detail='No file found')

    finally:
        driver.quit()

def _get_response_body(driver: webdriver.Chrome, request_id: float, max_retries: int = 5, delay: int = 1):
    for attempt in range(max_retries):
        try:
            return driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
        except WebDriverException as e:
            logging.info(f'Attempt {attempt + 1}: Failed to get response body - {e}')
            time.sleep(delay)

    raise ScrapeException(message='No resource with given identifier found')

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    error_message = {
        'error': 'Internal Server Error',
        'message': 'Unknown Error Occurred',
        'detail': str(exc),
        'path': str(request.url),
    }

    return JSONResponse(
        status_code=500,
        content=error_message
    )


@app.exception_handler(ScrapeException)
async def internal_server_error_handler(request: Request, exc: ScrapeException):
    error_message = {
        "error": "Scraping Error",
        "message": exc.message,
        "path": str(request.url),
    }

    return JSONResponse(
        status_code=500,
        content=error_message
    )


if __name__ == "__main__":
    uvicorn.run(app, host=configuration.host, port=configuration.port)
