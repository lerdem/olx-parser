import unittest
from unittest.mock import MagicMock

from requests import Session, HTTPError, ConnectionError

from ad.adapters.provider import _get_olx_search_html_base
from ad.core.errors import AdapterError


class Test(unittest.TestCase):
    def test_error1(self):
        fake_session_respone = MagicMock(
            **{'raise_for_status.side_effect': HTTPError('lol', '123')},
            autospec=Session
        )  # session object
        session = MagicMock(
            **{'get.return_value': fake_session_respone}, autospec=Session
        )  # session object
        with self.assertRaises(AdapterError):
            _get_olx_search_html_base('http://fake.com', session)

    def test_error2(self):
        session = MagicMock(
            **{'get.side_effect': ConnectionError('lol', '123')}, autospec=Session
        )  # session object
        with self.assertRaises(AdapterError):
            _get_olx_search_html_base('http://fake.com', session)
