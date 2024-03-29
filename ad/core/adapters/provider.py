from abc import ABC, abstractmethod
from typing import List, Tuple


class CreateAdsProvider(ABC):
    @abstractmethod
    def get_raw(self, start_url) -> List[Tuple]:  # or raises AdapterError
        pass


class DetailedAdProvider(ABC):
    @abstractmethod
    def get_raw(
        self, external_url
    ) -> Tuple[List, str, str, str]:  # or raises AdapterError
        pass


class PhoneProvider(ABC):
    @abstractmethod
    def get_raw(self, external_id) -> str:  # or raises AdapterError
        pass
