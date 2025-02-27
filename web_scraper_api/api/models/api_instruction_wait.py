from pydantic import BaseModel, Field

from api.enums.api_instruction_element_type import ApiInstructionElementType
from api.enums.api_instruction_identificator_type import ApiInstructionIdentificatorType


class ApiInstructionWait(BaseModel):
    seconds: int = Field()
    id: str = Field()
    by: ApiInstructionIdentificatorType = Field()
    wait_for: ApiInstructionElementType = Field()
