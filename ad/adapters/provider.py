from typing import List, Tuple, Dict
import requests
from lxml import etree

from ad.core.adapters.provider import CreateProvider, DetailProvider
from ad.core.errors import AdapterError


class _CreateProviderOlx1(CreateProvider):
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


class _CreateProviderOlx2(CreateProvider):
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


_SPECIAL = 'special'
_REGULAR = 'regular'

_mapper: Dict[str, CreateProvider] = {
    _SPECIAL: _CreateProviderOlx1,
    _REGULAR: _CreateProviderOlx2,
}


class CreateProviderOlx(CreateProvider):
    def get_raw(self, start_url) -> List[Tuple]:
        _provider_type = _SPECIAL if '/d/' in start_url else _REGULAR
        provider = _mapper[_provider_type]
        return provider().get_raw(start_url)


class GetItemProvider(DetailProvider):
    def get_raw(self, external_url) -> Tuple[List, str, str, str]:
        html = _get_olx_search_html(external_url)
        dom = etree.HTML(html)
        images = dom.xpath(
            './/div[contains(@data-cy, "adPhotos-swiperSlide")]/div/img/@data-src'
        )  # ['https://ireland.apollo.olxcdn.com:443/v1/files/nupcplxvi2jq1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/7lpzpaq405mp2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/y37d3uyelph8-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/etd6yxp26bmy2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/jjhriex63vas-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/lwy4lypf7dkz1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/7h2ih0zor3i82-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/pb9625qutphn3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/hln7nl1o80093-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/8sy3w6gcrgpv-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/86jl0gndg0jk3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/fhmeq8g1oj892-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/z7kc52gy2gfc2-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/da8rehzbvmhm1-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/xp6ld5cj30632-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/xsksiuajfyvs3-UA/image;s=900x1600', 'https://ireland.apollo.olxcdn.com:443/v1/files/4kp8iqzbazqr2-UA/image;s=900x1600']
        promote_link = dom.xpath(
            './/a[contains(@data-testid, "promotion-link")]/@href'
        )[
            0
        ]  # ['https://www.olx.ua/bundles/promote/?bs=adpage_promote&id=725494662']
        ad_id = promote_link.split('id=')[-1]
        try:
            ad_id = str(int(ad_id))
        except ValueError:
            raise AdapterError('Не удалось распарсить id обьявления')
        description = dom.xpath(
            './/div[contains(@data-cy, "ad_description")]/div/text()'
        )[0]
        card = dom.xpath('.//div[contains(@data-cy, "seller_card")]')[0]
        name = card.xpath('.//h2/text()')[0]
        return images, ad_id, description, name


def _get_olx_search_html(url) -> str:
    r = requests.get(url)
    r.raise_for_status()
    return r.text


if __name__ == '__main__':
    GetItemProvider().get_raw(None)
