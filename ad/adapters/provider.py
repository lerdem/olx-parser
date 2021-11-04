from typing import List, Tuple
import requests

from ad.core.adapters.provider import CreateProvider, DetailProvider
from ad.core.errors import AdapterError

# from .session import OlxRequest
from lxml import etree


class CreateProviderOlx(CreateProvider):
    _search_url = 'https://www.olx.ua/d/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/dnepr/?currency=UAH&search[private_business]=private&search[order]=created_at%3Adesc&search[filter_float_price%3Ato]=7000&search[filter_float_total_area%3Afrom]=30&search[filter_float_total_area%3Ato]=1000&view=list'

    def get_raw(self) -> List[Tuple]:
        html = self._get_olx_search_html()
        # with open('test.html') as f:
        #     html = f.read()
        dom = etree.HTML(html)
        return [
            self.process_item(item)
            for item in dom.xpath('.//div[contains(@data-cy, "l-card")]')
        ]

    def _get_olx_search_html(self) -> str:
        r = requests.get(self._search_url, verify=False)
        r.raise_for_status()
        return r.text

    @staticmethod
    def process_item(item):
        # TODO parse per item
        title, dirty_price, *_ = item.xpath(
            './/p[contains(@class, "Text")]/text()'
        )  # ['сдам квартиру в днепре 12 квартал', '3 000 грн.', 'Днепр', '11 октября 2021 г.', '36 м²']
        default_link = 'https://www.olx.ua'
        link = default_link + item.xpath('./a/@href')[0]
        return title, dirty_price, link


class GetItemProvider(DetailProvider):
    def get_raw(self, external_url) -> Tuple[List, str, str, str]:
        html = self._get_olx_search_html(external_url)
        # with open('item.html') as f:
        #     html = f.read()
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

    def _get_olx_search_html(self, url) -> str:
        r = requests.get(url, verify=False)
        r.raise_for_status()
        return r.text


if __name__ == '__main__':
    GetItemProvider().get_raw(None)
