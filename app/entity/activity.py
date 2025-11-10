from dataclasses import dataclass
from typing import Optional


@dataclass
class ActivityEntity:
    """
    Entity класс для Activity
    """
    id: int
    name: str
    parent_id: Optional[int] = None

