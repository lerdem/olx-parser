import configparser
import csv
import os
from itertools import chain
from functools import partial
from typing import Dict, List
from requests import Session, HTTPError, ConnectionError
from requests.exceptions import ChunkedEncodingError
from telegram import Bot
from telegram.error import InvalidToken
from sqlitedict import SqliteDict # type: ignore [import-untyped]

from ad.adapters.utils import get_config, BASE_DIR
from ad.core.adapters.repository import (
    CreateAdsRepo,
    DetailedAdRepo,
    CreateAdsConfig,
    Configuration,
    Configurations,
    ViewsRepo,
    Sender,
    GetDetailedAdRepo,
)
from ad.core.entities import (
    BaseAd,
    DetailedAd,
    AnyAd,
    Views,
    View,
)
from ad.core.errors import AdapterError

_DB_PATH = BASE_DIR.joinpath('storage.sqlite')


def get_table(table_name: str) -> SqliteDict:
    """Helper to return a thread-safe dict-like connection to SQLite.
    autocommit=True makes sure writes are instantly persistent."""
    return SqliteDict(_DB_PATH, tablename=table_name, autocommit=True)


get_ads_table = partial(get_table, 'ads')


def _filter_by_tag(tag: str, items: List[AnyAd]) -> List[AnyAd]:
    return [ad for ad in items if ad.tag == tag]

class CreateAdsRepoSqlite(CreateAdsRepo):
    # --- CreateAdsRepo Interface ---
    def save(self, base_ads: List[BaseAd]) -> None:
        with get_ads_table() as db:
            for ad in base_ads:
                if ad.id in db:
                    existing = db[ad.id]
                    existing.update(ad.dict(exclude_unset=True))
                    db[ad.id] = existing
                else:
                    db[ad.id] = ad.dict()

    def get_all(self) -> List[BaseAd]:
        with get_ads_table() as db:
            return [BaseAd(**row) for row in db.values()]


class DetailedAdRepoSqlite(DetailedAdRepo, GetDetailedAdRepo):
    # --- DetailedAdRepo Interface ---
    def save_detail(self, detailed_ad: DetailedAd) -> None:
        with get_ads_table() as db:
            if detailed_ad.id in db:
                # It exists! Fetch it safely with bracket notation
                existing_data = db[detailed_ad.id]
                existing_data.update(detailed_ad.dict(exclude_unset=True))
                db[detailed_ad.id] = existing_data
            else:
                db[detailed_ad.id] = detailed_ad.dict()


    def get_base_ad_by_id(self, id: str) -> BaseAd:
        with get_ads_table() as db:
            if id in db:
                return BaseAd(**db[id])
            raise AdapterError(f'Не найдено объявление {id}')

    # --- GetDetailedAdRepo Interface ---
    def get_all(self) -> List[DetailedAd]:
        with get_ads_table() as db:
            return [DetailedAd(**row) for row in db.values() if 'image_urls' in row]

    def get_by_tag(self, tag: str) -> List[DetailedAd]:
        return _filter_by_tag(tag, self.get_all())


class CreateAdsConfigJson(CreateAdsConfig):
    def get_configuration(self) -> Configurations:
        return Configuration.parse_file('configuration.json').__root__

def _get_ad(random_id: str) -> DetailedAd:
    return DetailedAd(
        id=random_id,  # dont show in template
        tag='arenda-dnepr',  # dont show in template
        title='Сдам 2-х комнатную квартиру на длительный период - Днепр',
        parse_date='2021-11-04 12:58:45',
        url='https://www.olx.ua/d/obyavlenie/sdam-2-h-komnatnuyu-kvartiru-na-dlitelnyy-period-IDN7dzO.html',
        description='Сдам 2-х комнатную квартиру на длительный период для семейной пары в районе '
        '97 школы'
        ' (Ул. Братьев Трофимовых 40), 6 этаж 9-и этажного дома, не угловая, теплая, есть лоджия, застеклена.',
        image_urls=[
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
        ],
        external_id='725276749',
        name='Феликс',
        phone='+380995437751',
        is_active=True,
        view_cout=10,
        publication_date='2021-11-04 11:58:45',
    )

class GetDebugRepo(GetDetailedAdRepo):
    def get_all(self) -> List[DetailedAd]:
        return [_get_ad('bc516e2abb5445ae9d03128a7a911f8f')]

    def get_by_tag(self, tag: str) -> List[DetailedAd]:
        return _filter_by_tag(tag, self.get_all())


class GetTableDebugRepo(GetDebugRepo):

    def get_all_detail(self) -> List[DetailedAd]:
        return [_get_ad('11'), _get_ad('22'), _get_ad('1144'), _get_ad('1199'), ]


class ViewsRepoSqlite(ViewsRepo):
    def get_views_by_ids(self, ad_ids: List[str]) -> Views:
        with get_table('ad_views') as db:
            # Direct lookup is O(1) instead of reading an entire file into memory!
            return [View(**db[ad_id]) for ad_id in ad_ids if ad_id in db]

    def save_view(self, view: View) -> None:
        with get_table('ad_views') as db:
            db[view.id] = view.dict()


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
        config = get_config()
        try:
            return config.get('secrets', 'TELEGRAM_BOT_TOKEN')
        except configparser.NoOptionError:
            raise AdapterError(
                '''Нет токена для телеграм бота.
                В файле environment.ini в [secrets] укажите:
                TELEGRAM_BOT_TOKEN=Replace-with-your-token'''
            )

    @staticmethod
    def _get_chat_id() -> int:
        config = get_config()
        try:
            return config.getint('secrets', 'CHAT_ID')
        except ValueError:
            raise AdapterError('телеграм CHAT_ID должен состоять из цифр')


class NTFYPusher(Sender):
    def __init__(self):
        self.ntfy_full_url = self._get_url()

    def send_message(self, msg: str) -> None:
        s = Session()
        try:
            r = s.post(
                self.ntfy_full_url, data=msg.encode(encoding='utf-8')
            )
        except ConnectionError as e:
            raise AdapterError(f'{e}, проблемы с подключение к интернету')
        except ChunkedEncodingError as e:
            raise AdapterError(f'{e}, невозможно прочитать ответ от ntfy')

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise AdapterError(f'{e}, на этапе запроса к ntfy')

    @staticmethod
    def _get_url():
        config = get_config()
        try:
            return config.get('ntfy', 'URL')
        except configparser.NoOptionError:
            raise AdapterError('No push url')
