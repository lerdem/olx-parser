import datetime
import ipaddress
from typing import List

from jinja2 import Environment, FileSystemLoader
from premailer import transform
from rfeed import Feed, Item, Guid

from ad.adapters.utils import get_config
from ad.core.adapters import Presenter
from ad.core.entities import BaseAds, DetailedAds, FullAd, BaseAd
from ad.core.errors import AdapterError

_BASE_TEXT = 'RSS feed parsed from Olx'


class DetailedAdFeedPresenter(Presenter):
    def __init__(self):
        self._port: int = 12345
        self._host_ip: str = self._get_host_ip()

    def present(self, ads: DetailedAds):
        items = []
        for ad in ads:
            item = Item(
                guid=Guid(ad.id, isPermaLink=False),
                title=ad.title,
                link=ad.url,
                description=_get_detail(ad),
                author='lerdem',
                pubDate=ad.parse_date,
            )
            items.append(item)

        description = f'{ads[0].tag}: {_BASE_TEXT}' if ads else _BASE_TEXT
        title = ads[0].tag if ads else _BASE_TEXT
        feed = Feed(
            title=title,
            link=f'http://{self._host_ip}:{self._port}/detail-rss',
            description=description,
            language='ru-Ru',
            lastBuildDate=datetime.datetime.now(),
            items=items,
        )
        return feed.rss()

    @staticmethod
    def _get_host_ip() -> str:  # or raises AdapterError
        config = get_config()
        maybe_ip = config.get('general', 'IP')
        try:
            # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
            sure_ip = ipaddress.ip_address(maybe_ip)
        except ValueError as e:
            raise AdapterError(e)
        else:
            return str(sure_ip)


class BaseAdTelegramPresenter(Presenter):
    def present(self, ads: BaseAds) -> List[str]:
        return [self._ad_to_html(ad) for ad in ads]

    @staticmethod
    def _ad_to_html(ad: BaseAd) -> str:
        # .encode('utf8').decode('utf8') to fix telegram cyrilic rendering issues
        return f'''<a href='{ad.url}'>{ad.title}</a>'''.encode('utf8').decode('utf8')


def _get_detail(ad: FullAd) -> str:
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('description.html')
    html = template.render(ad=ad)
    inline_html = transform(html)
    return inline_html


if __name__ == '__main__':

    content = 'This is about page'

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('description.html')

    output = template.render(preview_url=content)
    print(output)
