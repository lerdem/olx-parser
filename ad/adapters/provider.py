from typing import List, Tuple, Dict, Type
import requests
from lxml import etree

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
        return [
            self._process_item(item)
            for item in dom.xpath('.//div[contains(@data-cy, "l-card")]')
        ]

    @staticmethod
    def _process_item(item):
        title, *_ = item.xpath(
            './/p[contains(@class, "Text")]/text()'
        )  # ['Сдам 2-х комнатную квартиру на длительный период', 'Днепр', '05 ноября 2021 г.', '45 м²']
        default_link = 'https://www.olx.ua'
        link = default_link + item.xpath('./a/@href')[0]
        dirty_price = item.xpath('.//p[contains(@class, "Text")]/span/text()')[0]
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
        dirty_price = item.xpath('.//span[@class="price-label"]/text()')[0]
        return title, dirty_price, link


_SPECIAL = '/d/'  # apartment ads
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
        return dom.xpath(
            './/div[contains(@data-cy, "adPhotos-swiperSlide")]/div/img/@data-src'
        )

    def get_ad_id(self, dom) -> str:  # or raises AdapterError
        # ['https://www.olx.ua/bundles/promote/?bs=adpage_promote&id=725494662']
        try:
            promote_link = dom.xpath(
                './/a[contains(@data-testid, "promotion-link")]/@href'
            )[0]
            ad_id = promote_link.split('id=')[-1]
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
        return dom.xpath('.//div[contains(@data-cy, "ad_description")]/div/text()')[0]

    def get_name(self, dom) -> str:
        card = dom.xpath('.//div[contains(@data-cy, "seller_card")]')[0]
        return card.xpath('.//h2/text()')[0]


class _DetailedAdRabotaProviderOlx(_BaseAdProviderOlx):
    def get_images(self, dom) -> List:
        return []

    def get_description(self, dom) -> str:
        # help https://www.scientecheasy.com/2019/08/xpath-axes.html/
        return dom.xpath('.//h2//following-sibling::div/p/text()')[0]

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


def _get_olx_search_html(url) -> str:
    r = requests.get(url)
    r.raise_for_status()
    return r.text


if __name__ == '__main__':
    url = 'https://www.olx.ua/obyavlenie/rabota/buhgalter-v-magazin-IDMOigt.html#874994eb0c'
    DetailedAdProviderOlx().get_raw(url)
