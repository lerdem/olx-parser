import datetime

from rfeed import Feed, Item

from ad.core.entities import BaseAds, DetailedAds


class FeedPresenter:
    def present(self, ads: BaseAds):
        items = []
        for ad in ads:
            item = Item(
                title=ad.title,
                link=ad.url,
                author='lerdem',
                # guid=Guid("http://www.example.com/articles/1"),
                pubDate=ad.parse_date,
            )
            items.append(item)

        description = f'{ ads[0].tag}: ' if ads else ''
        feed = Feed(
            title='Парсер объявлений olx.ua',
            link='http://127.0.0.1/rss',
            description=f'{description}rss from olx',
            language='ru-Ru',
            lastBuildDate=datetime.datetime.now(),
            items=items,
        )
        return feed.rss()


class FeedDetailedPresenter:
    def present(self, ads: DetailedAds):
        items = []
        for ad in ads:
            item = Item(
                title=ad.title,
                link=ad.url,
                description=index(ad.image_urls),
                author='lerdem',
                # guid=Guid("http://www.example.com/articles/1"),
                pubDate=ad.parse_date,
            )
            items.append(item)

        description = f'{ ads[0].tag}: ' if ads else ''
        feed = Feed(
            title='Парсер объявлений olx.ua(Детали)',
            link='http://127.0.0.1/rss',
            description=f'{description}rss from olx',
            language='ru-Ru',
            lastBuildDate=datetime.datetime.now(),
            items=items,
        )
        return feed.rss()


def _make_images(urls):
    template = '<img src="{url}" alt="preview">'
    return ' '.join([template.format(url=url) for url in urls])


def index(image_urls):
    str_images = _make_images(image_urls)
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {str_images}
</body>
</html>
    '''
