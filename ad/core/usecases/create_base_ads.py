import uuid
from datetime import datetime
from typing import List

import pytz

from ad.core.adapters.provider import CreateProvider
from ad.core.adapters.repository import CreateRepo
from ad.core.entities import BaseAd


def create(repository: CreateRepo, provider: CreateProvider) -> List[str]:
    raw = provider.get_raw()
    saved = repository.get_all()
    existed_urls = [ad.url for ad in saved]
    provider_ads = [
        BaseAd(
            id=uuid.uuid4().hex,
            title=f'{item[0]} - {item[1]}',
            publication_date='-empty-',
            parse_date=datetime.now(pytz.utc),
            url=item[2],
        )
        for item in raw
    ]
    new = [ad for ad in provider_ads if ad.url not in existed_urls]
    repository.save(saved + new)
    return [i.id for i in new]
