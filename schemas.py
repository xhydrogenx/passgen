from typing import Optional

from pydantic import BaseModel


class SKeyAdd(BaseModel):
    name: str
    description: Optional[str] = None


class SKey(SKeyAdd):
    id: int
