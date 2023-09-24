from pydantic import BaseModel


class CreateAds(BaseModel):
    title: str
    description: str
    owner: str
