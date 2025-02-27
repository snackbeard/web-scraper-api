from typing import Any, Optional
from pydantic import BaseModel, Field

from api.enums.api_instruction_action_type import ApiInstructionActionType


class ApiInstruction(BaseModel):
    action_type: ApiInstructionActionType = Field(description='action type')
    action_value: Optional[Any] = Field(description='action value', default=None)
    action_ignore_error: Optional[bool] = Field(description='action ignore an error', default=False)