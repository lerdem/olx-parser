from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class CreateProvider(ABC):
    @abstractmethod
    def get_raw(self) -> List[Dict]:
        pass


class DetailProvider(ABC):
    @abstractmethod
    def get_raw(self, external_url) -> Tuple[List, str, str, str]:
        pass


class PhoneProvider(ABC):
    @abstractmethod
    def get_raw(self, external_id) -> str:
        pass
