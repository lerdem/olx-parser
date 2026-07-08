from datetime import datetime
from typing import List, Union, TypeVar, Optional
from pydantic import BaseModel, HttpUrl


class BaseAd(BaseModel):
    id: str
    tag: str
    title: str
    parse_date: datetime
    url: HttpUrl
    is_active: bool
# TODO is_active False create new BaseAd
    @property
    def path(self):
        return self.url.path

class _DetailAd(BaseModel):
    description: str
    image_urls: List[HttpUrl]
    external_id: str
    name: str

    publication_date: datetime
    view_cout: int
    phone: Optional[str] = None

class DetailedAd(_DetailAd, BaseAd):
    pass


class View(BaseModel):
    id: str


AnyAd = TypeVar('AnyAd', bound=DetailedAd)
Views = List[View]
