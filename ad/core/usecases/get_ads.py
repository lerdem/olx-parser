from dataclasses import dataclass

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetRepo


@dataclass
class GetAdsUseCase:
    _repo: GetRepo
    _presenter: Presenter

    def __call__(self, tag: str):
        ads = self._repo.get_by_tag(tag) if tag is not None else self._repo.get_all()
        return self._presenter.present(ads)
