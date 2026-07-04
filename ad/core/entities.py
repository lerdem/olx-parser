from datetime import datetime
from typing import List, Union, TypeVar
from pydantic import BaseModel, HttpUrl


class BaseAd(BaseModel):
    id: str
    tag: str
    title: str
    parse_date: datetime
    url: HttpUrl


class _DetailAd(BaseModel):
    description: str
    image_urls: List[HttpUrl]
    external_id: str
    name: str


class Contact(BaseModel):
    # https://github.com/samuelcolvin/pydantic/issues/1551
    phone: str


class DetailedAd(_DetailAd, BaseAd):
    pass


class FullAd(Contact, DetailedAd):
    # def serialize_fields(self):
    pass


class View(BaseModel):
    id: str


DetailedAds = List[DetailedAd]
FullAds = List[FullAd]
AnyAd = TypeVar('AnyAd', bound=DetailedAd)
Views = List[View]
