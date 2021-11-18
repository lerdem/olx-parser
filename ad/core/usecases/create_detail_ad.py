from dataclasses import dataclass

from ad.core.adapters.provider import DetailProvider
from ad.core.adapters.repository import DetailRepo
from ad.core.entities import DetailedAd


@dataclass
class CreateDetailUseCase:
    _repository: DetailRepo
    _provider: DetailProvider

    def __call__(self, ad_id: str) -> None:
        base_ad = self._repository.get_base_ad_by_id(ad_id)
        raw = self._provider.get_raw(base_ad.url)
        detailed_ad = DetailedAd(
            image_urls=raw[0],
            external_id=raw[1],
            description=raw[2],
            name=raw[3],
            **base_ad.dict()
        )

        self._repository.save(detailed_ad)
