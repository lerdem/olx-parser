from dataclasses import dataclass

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetDetailedAdRepo


@dataclass
class GetAdsUseCase:
    _repo: GetDetailedAdRepo
    _presenter: Presenter

    def __call__(self, tag: str):
        ads = self._repo.get_by_tag(tag) if tag is not None else self._repo.get_all()
        last_30_ads = sorted(ads, key=lambda x: x.parse_date, reverse=True)[:30]
        return self._presenter.present(last_30_ads)
