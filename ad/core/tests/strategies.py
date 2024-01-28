from datetime import datetime
from itertools import cycle
import hypothesis.strategies as st


from ad.core.entities import BaseAd, DetailedAd

_URLS = [
    'https://www.olx.ua/d/uk/obyavlenie/kvartira-v-arendu-brznka-karavan-klochko-lvoberezhniy-IDUeFir.html',
    'https://www.olx.ua/d/uk/obyavlenie/sdam-2-h-kvartiru-levyy-bereg-kosiora-pravda-IDTX3ZS.html',
    'https://www.olx.ua/d/uk/obyavlenie/sdam-2k-kvartiru-pr-mira-IDUdKIe.html',
    'https://www.olx.ua/d/uk/obyavlenie/sdam-2-komnatnuyu-levoberezhnyy-3-karavan-IDUdZfi.html',
    'https://www.olx.ua/d/uk/obyavlenie/kvartira-na-levoberezhnom-v-arendu-ne-rltor-IDSrbyI.html',
    'https://www.olx.ua/d/uk/obyavlenie/sdam-2-kom-kvartiru-donetskoe-shosse-134-klochko-6-berezinka-karavan-IDUeW72.html',
]
UrlSt = st.builds(lambda: next(cycle(_URLS)))
IdSt = st.text(alphabet='qwertyui1234567889', min_size=10, max_size=10)
TagSt = st.text(alphabet='qwertyuiop-asdfghjklzxcvbnm')
TitleSt = st.text()
ParseDateSt = st.datetimes(datetime.now())

BaseAdSt = st.builds(
    BaseAd, id=IdSt, tag=TagSt, title=TitleSt, parse_date=ParseDateSt, url=UrlSt
)

_IMAGE_URLS = [
    'https://ireland.apollo.olxcdn.com:443/v1/files/j31k5csrm9vp2-UA/image;s=854x384',
    'https://ireland.apollo.olxcdn.com:443/v1/files/jn6omphtsgad-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/zansrvj2uh673-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/k3uysaiiaevn-UA/image;s=854x384',
    'https://ireland.apollo.olxcdn.com:443/v1/files/vd624onnfj521-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/t3h4zijo2xds-UA/image;s=854x384',
    'https://ireland.apollo.olxcdn.com:443/v1/files/0usz5bi289vp2-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/jjdd7d35d8ca-UA/image;s=854x384',
    'https://ireland.apollo.olxcdn.com:443/v1/files/flbsr10fq6uh3-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/t1shs5579wxd2-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/k69e39fw5b0s1-UA/image;s=854x384',
    'https://ireland.apollo.olxcdn.com:443/v1/files/hknglo3p5c0a1-UA/image;s=384x854',
    'https://ireland.apollo.olxcdn.com:443/v1/files/90abhy3rgbdx1-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/9nwf5zho7ur73-UA/image;s=1600x1200',
    'https://ireland.apollo.olxcdn.com:443/v1/files/fkyfzffs04uc2-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/an642er892ys3-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/qk5iak4xq43n2-UA/image;s=1600x1200',
    'https://ireland.apollo.olxcdn.com:443/v1/files/9pb0ssxp4zan3-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/2juha7qyu52g3-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/tf2wgvjespxm-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/qlbavct2iycx2-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/ejke0r2rnx553-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/qpy48jmoaqzc1-UA/image;s=1200x1600',
    'https://ireland.apollo.olxcdn.com:443/v1/files/8dbgdbn6mems1-UA/image;s=1200x1600',
]

ImageUrlsSt = st.lists(
    st.builds(lambda: next(cycle(_IMAGE_URLS))), min_size=1, max_size=4
)
DetailedAdSt = st.builds(
    DetailedAd,
    id=IdSt,
    tag=TagSt,
    title=TitleSt,
    parse_date=ParseDateSt,
    url=UrlSt,
    description=TitleSt,
    image_urls=ImageUrlsSt,
    external_id=st.text(alphabet='1234567890', min_size=8, max_size=8),
    name=TitleSt,
)

if __name__ == '__main__':
    ad = BaseAdSt.example()
    ad2 = DetailedAdSt.example()
    from pprint import pprint

    pprint(ad)
    pprint(ad2)
