from dataclasses import dataclass
from typing import Optional, Dict

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetDetailedAdRepo, ViewsRepo, Sender
from ad.core.entities import View, DetailedAds
from ad.core.errors import AdapterError, UseCaseError


@dataclass
class AdsSenderUseCase:
    _ads_repository: GetDetailedAdRepo
    _views_repository: ViewsRepo
    _sender: Sender
    _presenter: Presenter

    def execute(self, tag: Optional[str]) -> None:
        ads = (
            self._ads_repository.get_by_tag(tag)
            if tag is not None
            else self._ads_repository.get_all()
        )
        ads_ids = [ad.id for ad in ads]
        views = self._views_repository.get_views_by_ids(ads_ids)
        views_ids = [view.id for view in views]
        unsent_ads_ids = set(ads_ids) - set(views_ids)

        ads_d: Dict[str:DetailedAds] = {ad.id: ad for ad in ads}
        unsent_ads: DetailedAds = [ads_d[unsent_ads_id] for unsent_ads_id in unsent_ads_ids]

        messages = self._presenter.present(unsent_ads)
        for message, unsent_ad in zip(messages, unsent_ads):
            try:
                self._sender.send_message(message)
            except AdapterError as e:
                raise UseCaseError(f'Ошибка при отправке сообщения: {e}')
            self._views_repository.save_view(View(id=unsent_ad.id))
