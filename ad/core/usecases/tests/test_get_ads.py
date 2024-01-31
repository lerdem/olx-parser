import unittest
from unittest.mock import create_autospec

import hypothesis.strategies as st
from hypothesis import given, example, assume, settings, HealthCheck

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetDetailedAdRepo
from ad.core.entities import BaseAds
from ad.core.tests.strategies import DetailedAdSt
from ad.core.usecases.get_ads import GetAdsUseCase, _stop_word_ignore


class TestGetAdsUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ads_repo = create_autospec(GetDetailedAdRepo)
        self.presenter = create_autospec(Presenter)

    @given(st.lists(DetailedAdSt, unique_by=lambda x: x.id, min_size=1, max_size=30))
    def test_usecase_ok(self, return_repo):
        self.ads_repo.reset_mock()  # hypothesis dont reset mocks
        self.presenter.reset_mock()  # hypothesis dont reset mocks
        self.ads_repo.get_all.return_value = return_repo

        get_ads = GetAdsUseCase(_repo=self.ads_repo, _presenter=self.presenter)
        get_ads(tag=None, stop_words=None)
        presenter_call_arg: BaseAds = self.presenter.present.call_args_list[0][0][0]
        self.assertEqual(len(presenter_call_arg), len(return_repo))

    @example(text='Сдам 2х комнатную квартиру по улице Тепличная', is_ignore=True)
    @example(
        text='Сдам 2 кімнатну квартиру, у кінеці пр. Слобожанське, вул. Киснева 2',
        is_ignore=False,
    )
    @given(
        text=st.just('Сдам 2-ком. Квартиру. Калиновой и Образцова. 4/9 Эт.'),
        is_ignore=st.just(False),
    )
    def test_stop_word_ignore(self, text, is_ignore):
        res = _stop_word_ignore(['вул. Киснева', 'Образцова'], text)
        self.assertIs(
            res, is_ignore, msg='если есть совпадение, то возвращаеться False'
        )
