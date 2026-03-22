from pydantic import BaseModel, HttpUrl


class CreateUrl(BaseModel):
    original_url: HttpUrl
    model_config = {"from_attributes": True}


class ReadUrl(BaseModel):
    original_url: HttpUrl
    model_config = {"from_attributes": True}


class ShortUrl(BaseModel):
    short_id: str
    model_config = {"from_attributes": True}
