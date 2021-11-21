from abc import ABC, abstractmethod


class Presenter(ABC):
    @abstractmethod
    def present(self, ads):
        pass
