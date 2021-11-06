from flask import Flask, Response, render_template

from ad.adapters.presenter import FeedPresenter, FeedDetailedPresenter
from ad.adapters.repository import GetRepoCsv, GetDetailedRepoCsv
from ad.core.entities import FullAd
from ad.core.usecases.get_ads import get

app = Flask(__name__)


@app.route('/rss')
def hello_world():
    data = get(GetRepoCsv(), FeedPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/detail-rss')
def detail_rss():
    data = get(GetDetailedRepoCsv(), FeedDetailedPresenter())
    return Response(data, headers={'Content-Type': 'application/rss+xml'})


@app.route('/debug-template')
def debug_template():
    ad = FullAd(
        id='bc516e2abb5445ae9d03128a7a911f8f',  # dont show in template
        title='Сдам 2-х комнатную квартиру на длительный период - Днепр',
        publication_date='2021-11-04 12:58:45',  # dont show in template
        parse_date='2021-11-04 12:58:45',
        url='https://www.olx.ua/d/obyavlenie/sdam-2-h-komnatnuyu-kvartiru-na-dlitelnyy-period-IDN7dzO.html',
        description='Сдам 2-х комнатную квартиру на длительный период для семейной пары в районе '
        '97 школы'
        ' (Ул. Братьев Трофимовых 40), 6 этаж 9-и этажного дома, не угловая, теплая, есть лоджия, застеклена.',
        image_urls=[
            'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/vssv777gydrg-UA/image;s=2000x1500',
            'https://ireland.apollo.olxcdn.com:443/v1/files/21lvfbjvx6jx1-UA/image;s=4000x3000',
            'https://ireland.apollo.olxcdn.com:443/v1/files/9dehurvrn1ue2-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/fvr23veakqja1-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/svrkipcuf3r71-UA/image;s=2000x1496',
            'https://ireland.apollo.olxcdn.com:443/v1/files/6n39w43g0gmj-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/10ptsjo4ljri3-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/9yvwzufag4pi2-UA/image;s=2000x1496',
            'https://ireland.apollo.olxcdn.com:443/v1/files/44zp0l4nwjig1-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/2jsoxcvueqek1-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/ky0gykw1ttx83-UA/image;s=2000x1496',
            'https://ireland.apollo.olxcdn.com:443/v1/files/4qqjumeu5inp1-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/tv6t37n93odb3-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/dumns992d4rd-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/eizp1ic23hap2-UA/image;s=3016x4032',
            'https://ireland.apollo.olxcdn.com:443/v1/files/v8zxndhkadxd2-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/pk8d5j5vjpff-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/l6in3x6fu2601-UA/image;s=3016x4032',
            'https://ireland.apollo.olxcdn.com:443/v1/files/lifu0k7sen3q3-UA/image;s=3016x4032',
            'https://ireland.apollo.olxcdn.com:443/v1/files/cjxyk2p39syr2-UA/image;s=4032x3016',
            'https://ireland.apollo.olxcdn.com:443/v1/files/l6k4isbcipss3-UA/image;s=4032x3016',
        ],
        external_id='725276749',
        name='Феликс',
        phone='+380995437751',
    )
    return render_template('description.html', ad=ad)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=12345)
