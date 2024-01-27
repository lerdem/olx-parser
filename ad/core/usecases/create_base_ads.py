import uuid
from dataclasses import dataclass
from datetime import datetime
from operator import add
from typing import List
from functools import reduce
import pytz

from ad.core.adapters.provider import CreateAdsProvider
from ad.core.adapters.repository import CreateAdsRepo, CreateAdsConfig
from ad.core.entities import BaseAd
from ad.core.errors import AdapterError, UseCaseError


@dataclass
class CreateAdsUseCase:
    _repository: CreateAdsRepo
    _provider: CreateAdsProvider
    _configuration: CreateAdsConfig

    def __call__(self) -> List[str]:
        # TODO проблема, если 2 из 10 url падает, то дальше не идет загрузка.
        confs = self._configuration.get_configuration()
        return reduce(
            add, [self.__process_one(conf.search_url, conf.tag) for conf in confs], []
        )

    def __process_one(self, url: str, tag: str) -> List[str]:
        try:
            raw = self._provider.get_raw(start_url=url)
        except AdapterError as e:
            raise UseCaseError(
                f'Ошибка при получении "raw" данных: {e}.\nFor debug url={url}, tag={tag}'
            )
        saved = self._repository.get_all()
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
        self._repository.save(new)
        return [i.id for i in new]
