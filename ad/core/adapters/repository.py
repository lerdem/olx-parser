from abc import ABC, abstractmethod
from typing import List, MutableSequence
from pydantic import BaseModel, HttpUrl, root_validator

from ad.core.entities import BaseAds, DetailedAd, BaseAd


class CreateAdsRepo(ABC):
    @abstractmethod
    def save(self, base_ads: BaseAds) -> None:
        pass

    @abstractmethod
    def get_all(self) -> BaseAds:
        pass


class DetailedAdRepo(ABC):
    @abstractmethod
    def save(self, detailed_ad: DetailedAd) -> None:
        pass

    @abstractmethod
    def get_base_ad_by_id(self, id: str) -> BaseAd:
        pass


class GetRepo(ABC):
    @abstractmethod
    def get_all(self) -> BaseAds:
        pass

    @abstractmethod
    def get_by_tag(self, tag: str) -> BaseAds:
        pass


class _ConfigurationItem(BaseModel):
    search_url: HttpUrl
    tag: str


Configurations = List[_ConfigurationItem]


class Configuration(BaseModel):
    __root__: Configurations

    @root_validator
    def check_tag_unique(cls, values):
        confs = values['__root__']
        _is_unique_by([i.tag for i in confs], 'tags list')
        _is_unique_by([i.search_url for i in confs], 'urls list')
        return values


def _is_unique_by(values: MutableSequence, values_name: str):
    if len(values) != len(set(values)):
        raise ValueError(f'{values_name} should be unique')


class CreateAdsConfig(ABC):
    @abstractmethod
    def get_configuration(self) -> Configurations:
        pass
