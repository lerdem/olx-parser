import configparser
import csv
import os
from itertools import chain
from pathlib import Path
from typing import Dict, List
from telegram import Bot
from telegram.bot import InvalidToken

from ad.core.adapters.repository import (
    CreateAdsRepo,
    GetRepo,
    DetailedAdRepo,
    CreateAdsConfig,
    Configuration,
    Configurations,
    ViewsRepo,
    Sender,
)
from ad.core.entities import (
    BaseAds,
    BaseAd,
    FullAd,
    DetailedAd,
    DetailedAds,
    AnyAds,
    FullAds,
    Views,
    View,
)
from ad.core.errors import AdapterError

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

_BASE_FILE_NAME = BASE_DIR.joinpath('.base-ads.csv')
_DETAIL_FILE_NAME = BASE_DIR.joinpath('.detail-ads.csv')
_FULL_FILE_NAME = BASE_DIR.joinpath('.full-ads.csv')
_VIEWS_FILE_NAME = BASE_DIR.joinpath('.ad-views.csv')

_file_field_map = {
    _BASE_FILE_NAME: BaseAd.__fields__.keys(),
    _DETAIL_FILE_NAME: DetailedAd.__fields__.keys(),
    _FULL_FILE_NAME: FullAd.__fields__.keys(),
    _VIEWS_FILE_NAME: View.__fields__.keys(),
}


def _init_storage(file_name, fields):
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def _migrate():
    for file_name, fields in _file_field_map.items():
        _init_storage(file_name, fields)


class CreateAdsRepoCsv(CreateAdsRepo):
    def save(self, base_ads: BaseAds) -> None:
        with open(_BASE_FILE_NAME, 'a', newline='') as csvfile:
            fieldnames = BaseAd.__fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for ad in base_ads:
                writer.writerow(ad.dict())

    def get_all(self) -> BaseAds:
        with open(_BASE_FILE_NAME) as csvfile:
            reader = csv.DictReader(csvfile)
            return [BaseAd(**row) for row in reader]


class DetailedAdRepoCsv(DetailedAdRepo):
    def save(self, detailed_ad: DetailedAd) -> None:
        saved = self.get_all_detail()
        with open(_DETAIL_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = DetailedAd.__fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ad in self._mix_existed_ads_and_one_new(saved, detailed_ad):
                writer.writerow(_serialize_detail(ad))

    @staticmethod
    def _mix_existed_ads_and_one_new(
        existed_ads: DetailedAds, new_or_updated_ad: DetailedAd
    ):
        existed_ads_without_new = filter(
            lambda x: x.external_id != new_or_updated_ad.external_id, existed_ads
        )
        for ad in chain(existed_ads_without_new, [new_or_updated_ad]):
            yield ad

    @staticmethod
    def get_all_detail() -> DetailedAds:
        with open(_DETAIL_FILE_NAME) as csvfile:
            reader = csv.DictReader(csvfile)
            return [_deserialize_detail(row) for row in reader]

    @staticmethod
    def get_all_base() -> BaseAds:
        return CreateAdsRepoCsv().get_all()

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


class GetBaseAdRepoCsv(GetRepo):
    def get_all(self) -> BaseAds:
        return CreateAdsRepoCsv().get_all()

    def get_by_tag(self, tag: str) -> BaseAds:
        return _filter_by_tag(tag, self.get_all())


class DetailedAdGetRepoCsv(GetRepo):
    def get_all(self) -> DetailedAds:
        return DetailedAdRepoCsv().get_all_detail()

    def get_by_tag(self, tag: str) -> DetailedAds:
        return _filter_by_tag(tag, self.get_all())


def _filter_by_tag(tag, items: AnyAds) -> AnyAds:
    return [ad for ad in items if ad.tag == tag]


class CreateAdsConfigJson(CreateAdsConfig):
    def get_configuration(self) -> Configurations:
        return Configuration.parse_file('configuration.json').__root__


class GetDebugRepo(GetRepo):
    def get_all(self) -> FullAds:
        ad = FullAd(
            id='bc516e2abb5445ae9d03128a7a911f8f',  # dont show in template
            tag='arenda-dnepr',  # dont show in template
            title='Сдам 2-х комнатную квартиру на длительный период - Днепр',
            publication_date='2021-11-04 12:58:45',  # dont show in template
            parse_date='2021-11-04 12:58:45',
            url='https://www.olx.ua/d/obyavlenie/sdam-2-h-komnatnuyu-kvartiru-na-dlitelnyy-period-IDN7dzO.html',
            description='Сдам 2-х комнатную квартиру на длительный период для семейной пары в районе '
            '97 школы'
            ' (Ул. Братьев Трофимовых 40), 6 этаж 9-и этажного дома, не угловая, теплая, есть лоджия, застеклена.',
            image_urls=[
                'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
                'https://ireland.apollo.olxcdn.com/v1/files/pxokmbrmwf9v2-UA/image;s=1104x1472',
                'https://ireland.apollo.olxcdn.com/v1/files/ve9s1d20cn211-UA/image;s=1104x1472',
                'https://ireland.apollo.olxcdn.com/v1/files/ralzthng8yp52-UA/image;s=1944x2592',
                'https://ireland.apollo.olxcdn.com/v1/files/il2y84fnyo5w-UA/image;s=591x1280',
            ],
            external_id='725276749',
            name='Феликс',
            phone='+380995437751',
        )
        return [ad]

    def get_by_tag(self, tag: str) -> DetailedAds:
        return _filter_by_tag(tag, self.get_all())


class ViewsRepoCsv(ViewsRepo):
    def get_views_by_ids(self, ad_ids: List[str]) -> Views:
        # ad_ids = [0,1,2,3] views = [1,2] return [1,2]
        with open(_VIEWS_FILE_NAME) as csvfile:
            reader = csv.DictReader(csvfile)
            all_ad_views = [View(**row) for row in reader]
            all_ad_views_d = {view.id: view for view in all_ad_views}
            viewed_ads_ids = set(ad_ids).intersection(set(all_ad_views_d.keys()))
            return [
                view
                for view_id, view in all_ad_views_d.items()
                if view_id in viewed_ads_ids
            ]

    def save_view(self, view: View) -> None:
        with open(_VIEWS_FILE_NAME, 'a', newline='') as csvfile:
            fieldnames = View.__fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(view.dict())


class TelegramSender(Sender):
    def __init__(self):
        _token = self._get_token()
        try:
            self._bot = Bot(token=_token)
        except InvalidToken:
            raise AdapterError('Нужен валидный телеграм токен, а не любые символы')
        self._chat_id = self._get_chat_id()

    def send_message(self, msg: str) -> None:
        self._bot.send_message(chat_id=self._chat_id, text=msg, parse_mode='HTML')

    @staticmethod
    def _get_token():
        config = TelegramSender._get_config()

        try:
            return config.get('secrets', 'TELEGRAM_BOT_TOKEN')
        except configparser.NoOptionError:
            raise AdapterError(
                '''Нет токена для телеграм бота.
                В файле environment.ini в [secrets] укажите:
                TELEGRAM_BOT_TOKEN=Replace-with-your-token'''
            )

    @staticmethod
    def _get_config():
        config_file = BASE_DIR.joinpath('environment.ini')
        config = configparser.ConfigParser()
        with open(config_file) as raw_config_file:
            config.read_file(raw_config_file)
        return config

    @staticmethod
    def _get_chat_id() -> int:
        config = TelegramSender._get_config()
        try:
            return config.getint('secrets', 'CHAT_ID')
        except ValueError:
            raise AdapterError('телеграм CHAT_ID должен состоять из цифр')


if __name__ == '__main__':
    _migrate()
