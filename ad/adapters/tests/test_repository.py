import unittest
from hypothesis import given


from ad.adapters.repository import (
    DetailedAdRepoCsv,
    _deserialize_detail,
    _serialize_detail,
)
from ad.core.entities import DetailedAd
from ad.core.tests.strategies import DetailedAdSt

_ad = DetailedAd(
    id='bc516e2abb5445ae9d03128a7a911f8f',  # dont show in template
    tag='arenda-dnepr',  # dont show in template
    title='Сдам 2-х комнатную квартиру на длительный период - Днепр',
    publication_date='2021-11-04 12:58:45',  # dont show in template
    parse_date='2021-11-04 12:58:45',
    url='https://www.olx.ua/d/obyavlenie/sdam-2-h-komnatnuyu-kvartiru-na-dlitelnyy-period-IDN7dzO.html',
    description='Сдам 2-х комнатную квартиру на длительный период для семейной пары в районе '
    '97 школы'
    ' (Ул. Братьев Трофимовых 40), 6 этаж 9-и этажного дома, не угловая, теплая, есть лоджия, застеклена.',
    image_urls=[
        'https://ireland.apollo.olxcdn.com:443/v1/files/dodwyas1emy32-UA/image;s=4000x3000',
        'https://ireland.apollo.olxcdn.com/v1/files/pxokmbrmwf9v2-UA/image;s=1104x1472',
        'https://ireland.apollo.olxcdn.com/v1/files/ve9s1d20cn211-UA/image;s=1104x1472',
        'https://ireland.apollo.olxcdn.com/v1/files/ralzthng8yp52-UA/image;s=1944x2592',
        'https://ireland.apollo.olxcdn.com/v1/files/il2y84fnyo5w-UA/image;s=591x1280',
    ],
    external_id='725276749',
    name='Феликс',
)
saved = [_ad]
new_or_updated_ad = DetailedAd(**_ad.dict())


class TestStringMethods(unittest.TestCase):
    def test_save(self):
        repo = DetailedAdRepoCsv()
        res = list(repo._mix_existed_ads_and_one_new(saved, new_or_updated_ad))
        self.assertListEqual(res, [new_or_updated_ad])

    @given(DetailedAdSt)
    def test_detail_serialization(self, detailed_ad):
        new_ad = _deserialize_detail(_serialize_detail(detailed_ad))
        self.assertEqual(new_ad, detailed_ad)


if __name__ == '__main__':
    unittest.main()
