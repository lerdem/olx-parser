import unittest
from unittest.mock import create_autospec

import hypothesis.strategies as st
from hypothesis import given, example, assume, settings

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetDetailedAdRepo, ViewsRepo, Sender
from ad.core.errors import AdapterError, UseCaseError
from ad.core.tests.strategies import BaseAdSt
from ad.core.usecases.ads_sender import AdsSenderUseCase


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.ads_repo = create_autospec(GetDetailedAdRepo)
        self.view_repo = create_autospec(ViewsRepo)
        self.sender = create_autospec(Sender)
        self.presenter = create_autospec(Presenter)

    @given(st.lists(BaseAdSt, unique_by=lambda x: x.id, max_size=10))
    @example(return_repo=[])
    def test_usecase_ok(self, return_repo):
        self._reset_mocks()  # hypothesis dont reset mocks
        self.ads_repo.get_all.return_value = return_repo
        view_repo = return_repo[:3]
        viewed_ads_count = len(view_repo)
        self.view_repo.get_views_by_ids.return_value = view_repo
        self.presenter.present.return_value = ['return_message'] * viewed_ads_count

        send_ads = AdsSenderUseCase(
            self.ads_repo, self.view_repo, self.sender, self.presenter
        )
        send_ads.execute(None)

        self.presenter.present.assert_called_once()
        self.assertEqual(
            self.sender.send_message.call_count, self.view_repo.save_view.call_count
        )
        self.assertGreaterEqual(viewed_ads_count, self.sender.send_message.call_count)

    def _reset_mocks(self):
        self.presenter.reset_mock()
        self.sender.reset_mock()
        self.view_repo.reset_mock()
        self.ads_repo.reset_mock()

    @given(BaseAdSt, BaseAdSt)
    @settings(max_examples=1)
    def test_usecase_error(self, _ad1, _ad2):
        assume(_ad1 != _ad2)
        self._reset_mocks()

        self.ads_repo.get_all.return_value = [_ad1, _ad2]
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
