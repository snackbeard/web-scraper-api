import uvicorn
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from selenium.webdriver.chrome.webdriver import WebDriver

from api.api_instruction_reader import ApiInstructionReader
from models.query import Query
from scraper.scraper import Scraper
from util.configuration import Configuration
from util.exceptions import ScrapeException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
configuration: Configuration = Configuration()

app: FastAPI = FastAPI()


@app.post(path='/api/v1/query', status_code=200, response_class=JSONResponse)
def scrape_webpage(query: Query, request: Request) -> dict[str, str]:
    if 'x-api-key' not in request.headers.keys() or request.headers.get('x-api-key') != configuration.api_key:
        raise HTTPException(status_code=403)

    driver: WebDriver = Scraper(configuration.driver_path).get(driver_options=query.options)
    driver.get(url=query.url)

    last_element = None

    try:
        for idx, instruction in enumerate(query.instructions):
            last_element = ApiInstructionReader().execute_instruction(instruction=instruction, driver=driver,
                                                                      element=last_element, instruction_index=idx)

        page_source: str = driver.page_source
        return {
            'response': page_source
        }
    finally:
        driver.quit()

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request):
    error_message = {
        'error': 'Internal Server Error',
        'message': 'Unknown Error Occurred',
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
