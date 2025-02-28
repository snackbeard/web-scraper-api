from pydantic import BaseModel, Field


class ApiInstructionWait(BaseModel):
    seconds: int = Field(description='seconds to wait')