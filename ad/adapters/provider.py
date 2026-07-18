import os
import pickle
import time
import random
import re
from contextlib import contextmanager
from os.path import join, exists
from pathlib import Path
from typing import List, Tuple, Dict, Type, Iterator, Any
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import dateparser
from lxml import etree
import lxml.etree as ET
import chompjs
from requests import Session, HTTPError, ConnectionError
from requests.exceptions import ChunkedEncodingError
from ratelimit import limits, sleep_and_retry

from ad.core.adapters.provider import (
    CreateAdsProvider,
    DetailedAdProvider,
    AvalabilityProvider
)
from ad.core.errors import AdapterError
from ad.logger import log_function_call


class _CreateProviderOlx1(CreateAdsProvider):
    _example_url = 'https://www.olx.ua/d/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/?currency=UAH&search[private_business]=private&search[order]=created_at%3Adesc&search[filter_float_price%3Ato]=7000&search[filter_float_total_area%3Afrom]=30&search[filter_float_total_area%3Ato]=1000&view=list'

    @log_function_call
    def get_raw(self, start_url) -> List[Tuple]:
        html = _get_olx_search_html(start_url)
        dom: Any = etree.HTML(html)
        is_empty_search = len(dom.xpath('//div[contains(@class, "emptynew")]')) == 1
        if is_empty_search:
            return []

        results = dom.xpath('.//div[contains(@data-testid, "listing-grid")]')

        # ipdb > rr, *hh = [0, 3]
        # ipdb > rr, hh
        # (0, [3])
        # ipdb > rr, *hh = [0]
        # ipdb > rr, hh
        # (0, [])
        # ipdb > rr, *hh = [0, 3, 4]
        # ipdb > rr, hh
        # (0, [3, 4])
        # поиск по району, *Подивіться результати для більшої відстані
        try:
            search_area, *larger_than_search_area = results
        except ValueError: #not enough values to unpack (expected at least 1, got 0)
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            raise AdapterError('Ничего нет в листинге')

        return [
            self._wraped_process_item(item)
            for item in search_area.xpath('.//div[contains(@data-cy, "l-card")]')
        ]

    @staticmethod
    def _process_item(item: Any) -> Tuple[str, str, str]:
        title = item.xpath('.//div[contains(@data-testid, "ad-card-title")]//h4/text()')[0]
        default_link = 'https://www.olx.ua'
        link = default_link + item.xpath('.//a/@href')[0]
        dirty_price = item.xpath('.//p[@data-testid="ad-price"]/text()')[0]  # '6 000 грн.'
        return title, dirty_price, link

    def _wraped_process_item(self, item: Any) -> Tuple[str, str, str]:
        try:
            data = self._process_item(item)
        except Exception as e:
            with open('item.pkl', 'wb') as f:
                pickle.dump(ET.tostring(item), f)
            raise
        else:
            return data

    @staticmethod
    def _restore():
        with open('item.pkl', 'rb') as f:
            item = ET.fromstring(pickle.load(f))

        import ipdb # type: ignore
        ipdb.set_trace()


class _CreateProviderOlx2(CreateAdsProvider):
    _example_url = 'https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/dnepr/q-pixel-4/'

    def get_raw(self, start_url) -> List[Tuple]:
        html = _get_olx_search_html(start_url)
        dom: Any = etree.HTML(html)
        is_empty_search = len(dom.xpath('//div[contains(@class, "emptynew")]')) == 1
        if is_empty_search:
            return []
        return [
            self._process_item(item)
            for item in dom.xpath('.//div[@class="offer-wrapper"]')
        ]

    @staticmethod
    def _process_item(item: Any):
        title = item.xpath('.//strong/text()')[0]
        link = item.xpath('.//a/@href')[0]
        dirty_price = item.xpath('.//p[@class="price"]/strong/text()')[0]
        return title, dirty_price, link


class _CreateProviderOlx3(_CreateProviderOlx2):
    _example_url = 'https://www.olx.ua/rabota/buhgalteriya/dnepr/?search%5Bfilter_enum_job_type%5D%5B0%5D=perm'

    @staticmethod
    def _process_item(item: Any):
        title = item.xpath('.//strong/text()')[0]
        link = item.xpath('.//a/@href')[0]
        try:
            dirty_price = item.xpath('.//span[@class="price-label"]/text()')[0]
        except IndexError:
            dirty_price = 'З/п не указана'
        return title, dirty_price, link


class _CreateProviderEH(CreateAdsProvider):
    _example_url = 'https://easyhata.ua/5097?business_type=rent&type=flat&city=3&district=7&sortable=-created_at'

    @log_function_call
    def get_raw(self, start_url) -> List[Tuple]:
        html = _get_olx_search_html(start_url)
        dom: Any = etree.HTML(html)

        script_tag = dom.xpath('//script[contains(text(), "realties")]')
        if not script_tag:
            raise AdapterError('нет scipt with realties')
        match = re.search(re.escape('realties:') + r'\s*(\[.*)', script_tag[0].text, re.DOTALL)
        if not match:
            raise AdapterError('нет js массива realties')
        raw_tail_string = match.group(1)
        results = chompjs.parse_js_object(raw_tail_string)

        return [
            self._wraped_process_item(item)
            for item in results
        ]

    @staticmethod
    def _process_item(item: Any) -> Tuple[str, str, str]:
        fragment = etree.HTML(item['text'])
        title = "\n".join([p.text for p in fragment.xpath('//p') if p.text])[:90]
        dirty_price = item['price']
        _id = item['id']
        link = f'https://easyhata.ua/flats/{_id}/rieltor/5097' # hardcode rieltorid 5097
        return title, dirty_price, link

    def _wraped_process_item(self, item: Any) -> Tuple[str, str, str]:
        try:
            data = self._process_item(item)
        except Exception as e:
            with open('item_2.pkl', 'wb') as f:
                pickle.dump(ET.tostring(item), f)
            raise
        else:
            return data

    @staticmethod
    def _restore():
        with open('item.pkl', 'rb') as f:
            item = ET.fromstring(pickle.load(f))

        import ipdb # type: ignore
        ipdb.set_trace()




_SPECIAL = '/nedvizhimost/'  # apartment ads
_REGULAR = 'regular'
_RABOTA = '/rabota/'
_EASY_HATA = 'easyhata'


_mapper_base: Dict[str, Type[CreateAdsProvider]] = {
    _SPECIAL: _CreateProviderOlx1,
    _RABOTA: _CreateProviderOlx3,
    _REGULAR: _CreateProviderOlx2,
    _EASY_HATA: _CreateProviderEH,
}


def _get_provider_klass(url, mapper) -> Type:
    for k in mapper:
        if k in url:
            return mapper[k]
    return mapper[_REGULAR]


class CreateProviderOlx(CreateAdsProvider):

    @sleep_and_retry
    @limits(calls=20, period=60)  # Ceiling: Max 20 requests per minute
    def get_raw(self, start_url) -> List[Tuple]:
        _provider_klass = _get_provider_klass(start_url, _mapper_base)
        return _provider_klass().get_raw(start_url)


class _BaseAdProviderOlx(DetailedAdProvider):
    def get_raw(self, external_url) -> Tuple[List, str, str, str, datetime, int]:
        html = _get_olx_search_html(external_url)
        dom: Any = etree.HTML(html)
        return (
            self.get_images(dom),
            self.get_ad_id(dom),
            self.get_description(dom),
            self.get_name(dom),
            self.get_publication_date(dom),
            self.get_view_count(dom),
        )

    def get_images(self, dom) -> List:
        # ['https://ireland.apollo.olxcdn.com:443/v1/files/nupcplxvi2jq1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/7lpzpaq405mp2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/y37d3uyelph8-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/etd6yxp26bmy2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/jjhriex63vas-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/lwy4lypf7dkz1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/7h2ih0zor3i82-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/pb9625qutphn3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/hln7nl1o80093-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/8sy3w6gcrgpv-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/86jl0gndg0jk3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/fhmeq8g1oj892-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/z7kc52gy2gfc2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/da8rehzbvmhm1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/xp6ld5cj30632-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/xsksiuajfyvs3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/4kp8iqzbazqr2-UA/image;s=900x1600']
        return dom.xpath('.//div[contains(@data-cy, "adPhotos-swiperSlide")]//img/@src')

    def get_ad_id(self, dom) -> str:  # or raises AdapterError
        # ['https://www.olx.ua/bundles/promote/?bs=adpage_promote&id=725494662']
        # ['/purchase/promote/variant/?ad-id=805426819&bs=adpage_promote']
        try:
            promote_link = dom.xpath(
                './/a[contains(@data-testid, "promotion-link")]/@href'
            )[0]
            ad_id = promote_link.split('ad-id=')[-1].split('&')[0]
        except IndexError:
            # for rabota ads https://www.olx.ua/obyavlenie/rabota/buhgalter-v-magazin-IDMOigt.html#874994eb0c
            ad_id = dom.xpath(
                './/div[contains(@data-cy, "ad-footer-bar-section")]/span/text()'
            )[-1]
        try:
            return str(int(ad_id))
        except ValueError:
            raise AdapterError('Не удалось распарсить id обьявления')

    def get_description(self, dom) -> str:
        # ['Сдаётся квартира общая площадь 45кв.м', '\nКалиновая(Образцова) . Квартира расположена на 2 этаже 5 этажного кирпичного дома.', '\nБез животных ', '\n06******44', '\n09******44']
        description_parts: List[str] = dom.xpath(
            './/div[contains(@data-cy, "ad_description")]/div/text()'
        )
        return ''.join(description_parts)

    def get_name(self, dom) -> str:
        card = dom.xpath('.//div[contains(@data-cy, "seller_card")]')[0]
        return card.xpath('.//h4/text()')[0]

    def get_publication_date(self, dom) -> datetime:
        # OLX render utc time and with some JS converts to KIEV time
        now = datetime.now(timezone.utc)
        settings = {
            'RELATIVE_BASE': now,
            'RETURN_AS_TIMEZONE_AWARE': True
        }
        raw: Any = dom.xpath('.//span[contains(@data-cy, "ad-posted-at")]')[0]
        # text returns ['Опубліковано ', 'сьогодні о 08:56']
        raw_date: str = raw.xpath('text()')[-1]
        when: datetime | None = dateparser.parse(raw_date, languages=['uk'], settings=settings)
        if when is None:
            raise AdapterError('Не удалось распарсить дату публикации')
        return when

    def get_view_count(self, dom) -> int:
        return 0


class _DetailedAdRabotaProviderOlx(_BaseAdProviderOlx):
    def get_images(self, dom) -> List:
        return []

    def get_description(self, dom) -> str:
        try:
            # help https://www.scientecheasy.com/2019/08/xpath-axes.html/
            return dom.xpath('.//h2//following-sibling::div/p/text()')[0]
        except IndexError:
            return 'Не удалось найти описание вакансии'

    def get_name(self, dom) -> str:
        # get from ad footer
        return dom.xpath('.//h2/text()')[-1]



class _DetailedAdProviderEH(DetailedAdProvider):
    def get_raw(self, external_url) -> Tuple[List, str, str, str, datetime, int]:
        html = _get_olx_search_html(external_url)
        dom: Any = etree.HTML(html)
        return (
            self.get_images(dom),
            self.get_ad_id(dom),
            self.get_description(dom),
            self.get_name(dom),
            self.get_publication_date(dom),
            self.get_view_count(dom),
        )

    def get_images(self, dom) -> List:
        return dom.xpath('.//div[contains(@class, "image-carousel__thumb-img")]/img/@src')

    def get_ad_id(self, dom) -> str:  # or raises AdapterError
        ad_id = dom.xpath('.//div[@class="rid__id"]/text()')[0].split('id: ')[-1]
        try:
            return str(int(ad_id))
        except ValueError:
            raise AdapterError('Не удалось распарсить id обьявления')

    def get_description(self, dom) -> str:
        return dom.xpath('.//div[@class="rid__description"]/p/text()')[0]

    def get_name(self, dom) -> str:
        return 'easyhata'

    def get_publication_date(self, dom) -> datetime:
        return datetime.now(timezone.utc)

    def get_view_count(self, dom) -> int:
        return 0


_mapper_detail: Dict[str, Type[DetailedAdProvider]] = {
    _RABOTA: _DetailedAdRabotaProviderOlx,
    _REGULAR: _BaseAdProviderOlx,
    _EASY_HATA: _DetailedAdProviderEH,
}


class DetailedAdProviderOlx(DetailedAdProvider):

    @sleep_and_retry
    @limits(calls=20, period=60)  # Ceiling: Max 20 requests per minute
    def get_raw(self, external_url) -> Tuple[List, str, str, str, datetime, int]:
        _provider_klass = _get_provider_klass(external_url, _mapper_detail)
        return _provider_klass().get_raw(external_url)


class _AvalabilityProviderOlx(AvalabilityProvider):

    def is_available(self, external_url) -> bool:
        try:
            _code = _get_olx_status_code(external_url)
        except AdapterError:
            return True # suppose its avaible
        if _code in (404, 410): # means OLX deactivate ad
            return False
        return True


class _AvalabilityProviderEH(AvalabilityProvider):

    def is_available(self, external_url) -> bool:
        html = _get_olx_search_html(external_url)
        dom: Any = etree.HTML(html)

        not_available = 'Здано' in dom.xpath('.//span[@class="app-button__inner"]/span/text()')[0]

        if not_available:
            return False
        return True

_mapper_avalability: Dict[str, Type[AvalabilityProvider]] = {
    _EASY_HATA: _AvalabilityProviderEH,
    'olx': _AvalabilityProviderOlx
}


class AvalabilityProviderAny(AvalabilityProvider):

    @sleep_and_retry
    @limits(calls=20, period=60)  # Ceiling: Max 20 requests per minute
    def is_available(self, external_url) -> bool:
        _provider_klass = _get_provider_klass(external_url, _mapper_avalability)
        time.sleep(random.uniform(0.5, 2.0)) # типо это не парсер
        return _provider_klass().is_available(external_url)


_BASE_DIR = Path(__file__).resolve(strict=True).parent


@contextmanager
def get_session() -> Iterator[Session]:
    # Ensure the target directory exists right away
    _dir = join(_BASE_DIR, 'ad', 'adapters')
    os.makedirs(_dir, exist_ok=True)

    _path = join(_dir, 'session.pickle')
    _tmp_path = join(_dir, 'session.pickle.tmp')

    # Safe Load
    if exists(_path) and os.path.getsize(_path) > 0:
        try:
            with open(_path, 'rb') as f:
                s = pickle.load(f)
        except Exception:
            s = Session()
    else:
        s = Session()
    try:
        yield s
    finally:
        # Safe Write
        with open(_tmp_path, 'wb') as f:
            pickle.dump(s, f)
        # Atomic Swap
        if exists(_tmp_path):
            os.replace(_tmp_path, _path)


def _get_olx_search_html(url) -> str:  # or raises AdapterError
    with get_session() as session:
        return _get_olx_search_html_base(url, session)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'X-Client': 'DESKTOP',
}

def _get_olx_search_html_base(url, session: Session) -> str:  # or raises AdapterError
    HEADERS['Referer'] = url
    try:
        r = session.get(url, headers=HEADERS)
    except ConnectionError as e:
        raise AdapterError(f'{e}, проблемы с подключение к интернету')
    except ChunkedEncodingError as e:
        raise AdapterError(f'{e}, невозможно прочитать ответ от ОЛХ')

    try:
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        raise AdapterError(f'{e}, на этапе запроса к ОЛХ')


def _get_olx_status_code(url) -> int:  # or raises AdapterError
    with get_session() as session:
        return _get_olx_404_base(url, session)


def _get_olx_404_base(url, session: Session) -> int:  # or raises AdapterError
    HEADERS['Referer'] = url
    try:
        r = session.head(url, headers=HEADERS, timeout=5)
    except ConnectionError as e:
        raise AdapterError(f'{e}, проблемы с подключение к интернету')
    except ChunkedEncodingError as e:
        raise AdapterError(f'{e}, невозможно прочитать ответ от ОЛХ')

    return r.status_code


if __name__ == '__main__':
    from pprint import pprint as print
    from ad.adapters.repository import CreateAdsConfigJson

    # config = CreateAdsConfigJson().get_configuration()[0]
    # print(config.search_url)
    # res = CreateProviderOlx().get_raw(config.search_url)
    # print(len(res))
    # print(res[0])
    # detail_url = res[0][2]
    # print(detail_url)
    # res = DetailedAdProviderOlx().get_raw('https://www.olx.ua/d/uk/obyavlenie/sdam-kvartiru-na-dlitelnyy-srok-ID10NIXy.html?isPreviewActive=0&search_reason=search%7Corganic&sliderIndex=0')
    # print(res)
    # docker exec -it olx-server python -m ad.adapters.provider
    # _CreateProviderOlx1._restore()
    # external_url = 'https://www.olx.ua/d/uk/obyavlenie/zdam-odnokmnatnu-kvartiru-vul-lipinskogo-ID10NOXp.html?search_reason=search%7Corganic'
    # res = AvalabilityProviderOlx().is_available(external_url)
    url = _CreateProviderEH._example_url
    res = CreateProviderOlx().get_raw(url)
    # det_url = 'https://easyhata.ua/flats/773300/rieltor/5097'
    # res = DetailedAdProviderOlx().get_raw(det_url)
    # url = 'https://easyhata.ua/flats/501834/rieltor/5097'
    # res= AvalabilityProviderAny().is_available(url)
    # print(res)
    # url = 'https://easyhata.ua/flats/773300/rieltor/5097'
    # res= AvalabilityProviderAny().is_available(url)
    print(res)
    # _CreateProviderEH()._restore()