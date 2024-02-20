import pickle
from contextlib import contextmanager
from os.path import join, exists
from pathlib import Path
from typing import List, Tuple, Dict, Type
from lxml import etree
from requests import Session, HTTPError, ConnectionError
from requests.exceptions import ChunkedEncodingError

from ad.core.adapters.provider import CreateAdsProvider, DetailedAdProvider
from ad.core.errors import AdapterError


class _CreateProviderOlx1(CreateAdsProvider):
    _example_url = 'https://www.olx.ua/d/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/?currency=UAH&search[private_business]=private&search[order]=created_at%3Adesc&search[filter_float_price%3Ato]=7000&search[filter_float_total_area%3Afrom]=30&search[filter_float_total_area%3Ato]=1000&view=list'

    def get_raw(self, start_url) -> List[Tuple]:
        html = _get_olx_search_html(start_url)
        dom = etree.HTML(html)
        is_empty_search = len(dom.xpath('//div[contains(@class, "emptynew")]')) == 1
        if is_empty_search:
            return []
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
        search_area, *larger_than_search_area = dom.xpath(
            './/div[contains(@data-testid, "listing-grid")]'
        )
        return [
            self._process_item(item)
            for item in search_area.xpath('.//div[contains(@data-cy, "l-card")]')
        ]

    @staticmethod
    def _process_item(item):
        title = item.xpath('.//h6/text()')[0]
        default_link = 'https://www.olx.ua'
        link = default_link + item.xpath('./a/@href')[0]
        dirty_price = item.xpath('.//p[@data-testid="ad-price"]/text()')[0] # '6 000 грн.'
        return title, dirty_price, link


class _CreateProviderOlx2(CreateAdsProvider):
    _example_url = 'https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/dnepr/q-pixel-4/'

    def get_raw(self, start_url) -> List[Tuple]:
        html = _get_olx_search_html(start_url)
        dom = etree.HTML(html)
        is_empty_search = len(dom.xpath('//div[contains(@class, "emptynew")]')) == 1
        if is_empty_search:
            return []
        return [
            self._process_item(item)
            for item in dom.xpath('.//div[@class="offer-wrapper"]')
        ]

    @staticmethod
    def _process_item(item):
        title = item.xpath('.//strong/text()')[0]
        link = item.xpath('.//a/@href')[0]
        dirty_price = item.xpath('.//p[@class="price"]/strong/text()')[0]
        return title, dirty_price, link


class _CreateProviderOlx3(_CreateProviderOlx2):
    _example_url = 'https://www.olx.ua/rabota/buhgalteriya/dnepr/?search%5Bfilter_enum_job_type%5D%5B0%5D=perm'

    @staticmethod
    def _process_item(item):
        title = item.xpath('.//strong/text()')[0]
        link = item.xpath('.//a/@href')[0]
        try:
            dirty_price = item.xpath('.//span[@class="price-label"]/text()')[0]
        except IndexError:
            dirty_price = 'З/п не указана'
        return title, dirty_price, link


_SPECIAL = '/nedvizhimost/'  # apartment ads
_REGULAR = 'regular'
_RABOTA = '/rabota/'


_mapper_base: Dict[str, Type[CreateAdsProvider]] = {
    _SPECIAL: _CreateProviderOlx1,
    _RABOTA: _CreateProviderOlx3,
    _REGULAR: _CreateProviderOlx2,
}


def _get_provider_klass(url, mapper) -> Type:
    for k in mapper:
        if k in url:
            return mapper[k]
    return mapper[_REGULAR]


class CreateProviderOlx(CreateAdsProvider):
    def get_raw(self, start_url) -> List[Tuple]:
        _provider_klass = _get_provider_klass(start_url, _mapper_base)
        return _provider_klass().get_raw(start_url)


class _BaseAdProviderOlx(DetailedAdProvider):
    def get_raw(self, external_url) -> Tuple[List, str, str, str]:
        html = _get_olx_search_html(external_url)
        dom = etree.HTML(html)
        return (
            self.get_images(dom),
            self.get_ad_id(dom),
            self.get_description(dom),
            self.get_name(dom),
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
        description_parts: List[str] = dom.xpath('.//div[contains(@data-cy, "ad_description")]/div/text()')
        return ''.join(description_parts)

    def get_name(self, dom) -> str:
        card = dom.xpath('.//div[contains(@data-cy, "seller_card")]')[0]
        return card.xpath('.//h4/text()')[0]


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


_mapper_detail: Dict[str, Type[DetailedAdProvider]] = {
    _RABOTA: _DetailedAdRabotaProviderOlx,
    _REGULAR: _BaseAdProviderOlx,
}


class DetailedAdProviderOlx(DetailedAdProvider):
    def get_raw(self, external_url) -> List[Tuple]:
        _provider_klass = _get_provider_klass(external_url, _mapper_detail)
        return _provider_klass().get_raw(external_url)


_BASE_DIR = Path(__file__).resolve(strict=True).parent


@contextmanager
def get_session() -> Session:
    _path = join(_BASE_DIR, 'session.pickle')
    if not exists(_path):
        s = Session()
    else:
        s: Session = pickle.load(open(_path, 'rb'))
    try:
        yield s
    finally:
        pickle.dump(s, open(_path, 'wb'))


def _get_olx_search_html(url)-> str: # or raises AdapterError
    with get_session() as session:
        return _get_olx_search_html_base(url, session)


def _get_olx_search_html_base(url, session: Session) -> str: # or raises AdapterError
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Referer': url,
        'X-Client': 'DESKTOP',
    }
    try:
        r = session.get(url, headers=headers)
    except ConnectionError as e:
        raise AdapterError(f'{e}, проблемы с подключение к интернету')
    except ChunkedEncodingError as e:
        raise AdapterError(f'{e}, невозможно прочитать ответ от ОЛХ')

    try:
        r.raise_for_status()
        return r.text
    except HTTPError as e:
        raise AdapterError(f'{e}, на этапе запроса к ОЛХ')



if __name__ == '__main__':
    from pprint import pprint as print
    from ad.adapters.repository import CreateAdsConfigJson

    config = CreateAdsConfigJson().get_configuration()[0]
    print(config.search_url)
    res = CreateProviderOlx().get_raw(config.search_url)
    print(len(res))
    print(res[0])
    detail_url = res[0][2]
    print(detail_url)
    res = DetailedAdProviderOlx().get_raw(detail_url)
    print(res)
