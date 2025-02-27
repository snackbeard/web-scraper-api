from pydantic import BaseModel, Field

from api.enums.api_instruction_block_type import ApiInstructionBlockType


class ApiInstructionScroll(BaseModel):
    block: ApiInstructionBlockType = Field()