import datetime
from typing import List

from jinja2 import Environment, FileSystemLoader

from rfeed import Feed, Item, Guid

from ad.core.adapters import Presenter
from ad.core.entities import BaseAds, DetailedAds, FullAd, BaseAd

_BASE_TEXT = 'rss from olx'


class DetailedAdFeedPresenter(Presenter):
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

        description = f'{ ads[0].tag}: {_BASE_TEXT}' if ads else _BASE_TEXT
        title = ads[0].tag if ads else _BASE_TEXT
        feed = Feed(
            title=title,
            link='http://127.0.0.1/rss',
            description=description,
            language='ru-Ru',
            lastBuildDate=datetime.datetime.now(),
            items=items,
        )
        return feed.rss()


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
    return template.render(ad=ad)


if __name__ == '__main__':

    content = 'This is about page'

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('description.html')

    output = template.render(preview_url=content)
    print(output)
