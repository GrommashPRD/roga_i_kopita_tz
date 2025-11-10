from pydantic import BaseModel, ConfigDict
from typing import Optional


class ActivityResponse(BaseModel):
    """
    Pydantic схме для Activity
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    parent_id: Optional[int] = None

