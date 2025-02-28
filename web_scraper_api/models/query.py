from typing import Optional

from pydantic import BaseModel, Field

from api.enums.api_instruction_content_type import ApiInstructionContentType
from api.models.api_driver_options import ApiDriverOptions
from api.models.api_instruction import ApiInstruction


class Query(BaseModel):
    url: str = Field(description='website url to scrape')
    content_type: Optional[ApiInstructionContentType] = Field(description='type of content to retrieve, either page source (html) or xhr content (json)', default=ApiInstructionContentType.PAGE_SOURCE)
    xhr_name: Optional[str] = Field(description='xhr file name to retrieve', default=None)
    options: Optional[ApiDriverOptions] = Field(description='contains user agent and browser options', default=None)
    instructions: Optional[list[ApiInstruction]] = Field(description='list of instructions on how to scrape a website', default=[])