from typing import Optional

from pydantic import BaseModel, Field


class ApiDriverOptions(BaseModel):
    user_agent: str = Field()
    options: Optional[list[str]] = Field(default=[])