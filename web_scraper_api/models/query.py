from typing import Optional

from pydantic import BaseModel, Field

from api.models.api_driver_options import ApiDriverOptions
from api.models.api_instruction import ApiInstruction


class Query(BaseModel):
    url: str = Field(description='website url to scrape')
    options: Optional[ApiDriverOptions] = Field(description='contains user agent and browser options', default=None)
    instructions: list[ApiInstruction] = Field(description='list of instructions on how to scrape a website')