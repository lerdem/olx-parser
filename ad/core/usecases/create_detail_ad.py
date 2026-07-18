from dataclasses import dataclass
from typing import Callable
from ad.core.adapters.provider import (
    DetailedAdProvider,
    AvalabilityProvider,
)
from ad.core.adapters.repository import (
    CreateAdsRepo,
    DetailedAdRepo,
    GetDetailedAdRepo
)
from ad.core.entities import DetailedAd, BaseAd
from ad.core.errors import AdapterError


@dataclass
class CreateDetailedAdUseCase:
    _repository: DetailedAdRepo
    _provider: DetailedAdProvider

    def __call__(self, ad_id: str) -> None:
        base_ad = self._repository.get_base_ad_by_id(ad_id)
        raw = self._provider.get_raw(base_ad.url)
        detailed_ad = DetailedAd(
            image_urls=raw[0],
            external_id=raw[1],
            description=raw[2],
            name=raw[3],
            publication_date=raw[4],
            view_cout=raw[5],
            **base_ad.dict()
        )

        self._repository.save_detail(detailed_ad)


@dataclass
class UploadDetailedAdsUseCase:
    _base_repo: CreateAdsRepo
    _get_repo: GetDetailedAdRepo
    _create_detail_uc: CreateDetailedAdUseCase

    def __call__(self) -> str:
        existed_base_ids = set([ad.id for ad in self._base_repo.get_all()])
        existed_detail_ids = set([ad.id for ad in self._get_repo.get_all()])
        need_to_update = existed_base_ids - existed_detail_ids
        if not need_to_update:
            return 'Нет объявлений для загрузки'
        for _id in need_to_update:
            try:
                self._create_detail_uc(_id)
            except AdapterError:
                print(f'SKIP: {_id}') # in case of 404/410
        return f'Загружено {len(need_to_update)} DetailedAd'


def _detail_to_base(detailed_ad: DetailedAd) -> BaseAd:
    base_ad_fields = BaseAd.__fields__.keys() # For Pydantic v1
    filtered_data = {k: v for k, v in detailed_ad.dict().items() if k in base_ad_fields}
    base_ad = BaseAd(**filtered_data)
    return base_ad


@dataclass
class DeactivationDetailedAdsUseCase:
    _base_repo: CreateAdsRepo
    _get_repo: GetDetailedAdRepo
    _detail_repo: DetailedAdRepo
    _provider: AvalabilityProvider

    def __call__(self) -> int:
        active_detailed_ads = [
            ad for ad in self._get_repo.get_all() if ad.is_active
        ]
        # TODO temp solution. Have to make checking by baches
        active_detailed_ads = sorted(active_detailed_ads, key=lambda x: x.publication_date, reverse=True)
        counter = 0
        for ad in active_detailed_ads:
            status = self._provider.is_available(ad.url)
            if status:
                continue
            disabled_ad = ad.copy(update={"is_active": False})
            self._detail_repo.save_detail(disabled_ad)
            self._base_repo.save([_detail_to_base(disabled_ad)])
            counter += 1
        return counter
