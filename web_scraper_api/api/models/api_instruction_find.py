from pydantic import BaseModel, Field

from api.enums.api_instruction_identificator_type import ApiInstructionIdentificatorType


class ApiInstructionFind(BaseModel):
    id: str = Field()
    by: ApiInstructionIdentificatorType = Field()