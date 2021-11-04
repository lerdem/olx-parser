import uuid
from datetime import datetime

from ad.core.adapters.provider import DetailProvider
from ad.core.adapters.repository import DetailRepo
from ad.core.entities import BaseAd, DetailedAd


def create_detail(ad_id: str, repository: DetailRepo, provider: DetailProvider):
    base_ad = repository.get_base_ad_by_id(ad_id)
    raw = provider.get_raw(base_ad.url)
    detailed_ad = DetailedAd(
        image_urls=raw[0],
        external_id=raw[1],
        description=raw[2],
        name=raw[3],
        **base_ad.dict()
    )

    repository.save(detailed_ad)
