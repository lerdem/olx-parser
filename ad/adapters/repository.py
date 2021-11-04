import csv
import os
from itertools import chain
from pathlib import Path
from typing import Dict

from ad.core.adapters.repository import CreateRepo, GetRepo, DetailRepo
from ad.core.entities import BaseAds, BaseAd, FullAd, DetailedAd, DetailedAds
from ad.core.errors import AdapterError

BASE_DIR = Path(__file__).resolve(strict=True).parent

_BASE_FILE_NAME = '.base-ads.csv'
_DETAIL_FILE_NAME = '.detail-ads.csv'
_FULL_FILE_NAME = '.full-ads.csv'

_file_field_map = {
    _BASE_FILE_NAME: BaseAd.__fields__.keys(),
    _DETAIL_FILE_NAME: DetailedAd.__fields__.keys(),
    _FULL_FILE_NAME: FullAd.__fields__.keys(),
}


def _init_storage(file_name, fields):
    if not os.path.exists(BASE_DIR.joinpath(file_name)):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def _migrate():
    for file_name, fields in _file_field_map.items():
        _init_storage(file_name, fields)


class CreateRepoCsv(CreateRepo):
    def save(self, base_ads: BaseAds) -> None:
        with open(_BASE_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = BaseAd.__fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ad in base_ads:
                writer.writerow(ad.dict())

    def get_all(self) -> BaseAds:
        with open(_BASE_FILE_NAME) as csvfile:
            reader = csv.DictReader(csvfile)
            return [BaseAd(**row) for row in reader]


class DetailRepoCsv(DetailRepo):
    def save(self, detailed_ad: DetailedAd) -> None:
        saved = self.get_all_detail()
        exclude_detailed = filter(lambda x: x.id != detailed_ad.id, saved)
        with open(_DETAIL_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = DetailedAd.__fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ad in chain(exclude_detailed, [detailed_ad]):
                writer.writerow(_serialize_detail(ad))

    @staticmethod
    def get_all_detail() -> DetailedAds:
        with open(_DETAIL_FILE_NAME) as csvfile:
            reader = csv.DictReader(csvfile)
            return [_deserialize_detail(row) for row in reader]

    @staticmethod
    def get_all_base() -> BaseAds:
        return CreateRepoCsv().get_all()

    def get_base_ad_by_id(self, id: str) -> BaseAd:
        try:
            return [x for x in self.get_all_base() if x.id == id][0]
        except IndexError:
            raise AdapterError(f'Не найдено объявление {id}')


def _serialize_detail(ad: DetailedAd) -> Dict:
    data = ad.dict()
    urls = _serialize_urls(data.pop('image_urls'))
    data['image_urls'] = urls
    return data


def _deserialize_detail(row: Dict) -> DetailedAd:
    raw = row.pop('image_urls')
    urls = _deserialize_urls(raw)
    row['image_urls'] = urls
    return DetailedAd(**row)


def _serialize_urls(urls):
    return ','.join(urls)


def _deserialize_urls(raw: str):
    if not raw:
        return []
    return raw.split(',')


class GetRepoCsv(GetRepo):
    def get_all(self) -> BaseAds:
        return CreateRepoCsv().get_all()


class GetDetailedRepoCsv(GetRepo):
    def get_all(self) -> BaseAds:
        return DetailRepoCsv().get_all_detail()


if __name__ == '__main__':
    _migrate()
