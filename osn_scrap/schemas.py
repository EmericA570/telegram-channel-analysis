from pydantic import BaseModel


class Message(BaseModel):
    text: str
    timestamp: str
    views: str
