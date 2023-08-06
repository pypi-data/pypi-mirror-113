from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    topic: str
    id: UUID = Field(default_factory=uuid4, init=False)
    created_at: datetime = Field(default_factory=datetime.now, init=False)
