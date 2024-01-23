from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetRepo, ViewsRepo, Sender
from ad.core.entities import BaseAd
from ad.core.errors import AdapterError, UseCaseError
from ad.core.usecases.ads_sender import AdsSenderUseCase
import unittest
from parameterized import parameterized
from unittest.mock import create_autospec


_ad1 = BaseAd(
    id='first-id',  # dont show in template
    tag='arenda-dnepr',  # dont show in template
    title='Сдам 2-х комнатную квартиру на длительный период - Днепр',
    parse_date='2021-11-04 12:58:45',
    url='https://www.olx.ua/d/obyavlenie/sdam-2-h-komnatnuyu-kvartiru-na-dlitelnyy-period-IDN7dzO.html',
)

_copy1 = _ad1.dict()
_copy1.pop('id')
_ad2 = BaseAd(id='second-id', **_copy1)
_ads = [_ad1, _ad2]


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.ads_repo = create_autospec(GetRepo)
        self.view_repo = create_autospec(ViewsRepo)
        self.sender = create_autospec(Sender)
        self.presenter = create_autospec(Presenter)

    @parameterized.expand(
        [
            (_ads, [_ad1], ['msg1'], 1, 1),
            (_ads, [], [], 1, 0),
            ([_ad1], [_ad1], [], 1, 0),
            (_ads, _ads, [], 1, 0),
        ]
    )
    def test_usecase_ok(
        self, return_repo, return_view, return_message, presenter_count, sender_count
    ):
        self.ads_repo.get_all.return_value = return_repo
        self.view_repo.get_views_by_ids.return_value = return_view
        self.presenter.present.return_value = return_message

        send_ads = AdsSenderUseCase(
            self.ads_repo, self.view_repo, self.sender, self.presenter
        )

        send_ads.execute(None)
        self.assertEqual(self.presenter.present.call_count, presenter_count)
        self.assertEqual(self.sender.send_message.call_count, sender_count)
        self.assertEqual(self.view_repo.save_view.call_count, sender_count)

    def test_usecase_error(self):
        self.ads_repo.get_all.return_value = _ads
        self.view_repo.get_views_by_ids.return_value = [_ad1]
        self.presenter.present.return_value = ['msg1']
        self.sender.send_message.side_effect = AdapterError

        send_ads = AdsSenderUseCase(
            self.ads_repo, self.view_repo, self.sender, self.presenter
        )
        with self.assertRaises(UseCaseError):
            send_ads.execute(None)

        self.sender.send_message.assert_called_once_with('msg1')
        self.view_repo.save_view.assert_not_called()
