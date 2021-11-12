import uuid
from datetime import datetime
from operator import add
from typing import List
from functools import partial, reduce
import pytz

from ad.core.adapters.provider import CreateProvider
from ad.core.adapters.repository import CreateRepo, ConfigRepo
from ad.core.entities import BaseAd


def create(
    repository: CreateRepo, provider: CreateProvider, configuration: ConfigRepo
) -> List[str]:
    confs = configuration.get_configuration()
    _reach_process_one = partial(_process_one, repository=repository, provider=provider)
    return reduce(
        add,
        [_reach_process_one(url=conf.search_url, tag=conf.tag) for conf in confs],
        [],
    )


def _process_one(
    repository: CreateRepo, provider: CreateProvider, url: str, tag: str
) -> List[str]:
    raw = provider.get_raw(start_url=url)
    saved = repository.get_all()
    existed_urls = [ad.url for ad in saved]
    provider_ads = [
        BaseAd(
            id=uuid.uuid4().hex,
            tag=tag,
            title=f'{item[0]} - {item[1]}',
            parse_date=datetime.now(pytz.utc),
            url=item[2],
        )
        for item in raw
    ]
    new = [ad for ad in provider_ads if ad.url not in existed_urls]
    repository.save(saved + new)
    return [i.id for i in new]
