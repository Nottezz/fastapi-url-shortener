from pydantic import BaseModel


class Health(BaseModel):
    status: str
    current_date: str
    current_uptime: int
    docs_url: str
