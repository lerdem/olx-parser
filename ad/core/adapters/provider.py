from datetime import datetime
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
    ) -> Tuple[List, str, str, str, datetime, int]:  # or raises AdapterError
        pass


class AvalabilityProvider(ABC):
    @abstractmethod
    def is_available(self, external_url) -> bool:
        pass
