from pydantic import BaseModel


class GetStats(BaseModel):
    visits: int
