from abc import ABC, abstractmethod

from ad.core.entities import BaseAds, DetailedAd, BaseAd


class CreateRepo(ABC):
    @abstractmethod
    def save(self, base_ads: BaseAds) -> None:
        pass

    @abstractmethod
    def get_all(self) -> BaseAds:
        pass


class DetailRepo(ABC):
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
