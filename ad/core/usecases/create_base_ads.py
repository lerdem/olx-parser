import uuid
from datetime import datetime
from typing import List

import pytz

from ad.core.adapters.provider import CreateProvider
from ad.core.adapters.repository import CreateRepo
from ad.core.entities import BaseAd


__URL_TO_MONITOR = 'https://www.olx.ua/d/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/?currency=UAH&search[private_business]=private&search[order]=created_at%3Adesc&search[filter_float_price%3Ato]=7000&search[filter_float_total_area%3Afrom]=30&search[filter_float_total_area%3Ato]=1000&view=list'


def create(repository: CreateRepo, provider: CreateProvider) -> List[str]:
    raw = provider.get_raw(__URL_TO_MONITOR)
    saved = repository.get_all()
    existed_urls = [ad.url for ad in saved]
    provider_ads = [
        BaseAd(
            id=uuid.uuid4().hex,
            title=f'{item[0]} - {item[1]}',
            parse_date=datetime.now(pytz.utc),
            url=item[2],
        )
        for item in raw
    ]
    new = [ad for ad in provider_ads if ad.url not in existed_urls]
    repository.save(saved + new)
    return [i.id for i in new]
