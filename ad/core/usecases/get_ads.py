import re
from dataclasses import dataclass
from functools import partial
from typing import List, Optional

from ad.core.adapters import Presenter
from ad.core.adapters.repository import GetDetailedAdRepo


@dataclass
class GetAdsUseCase:
    _repo: GetDetailedAdRepo
    _presenter: Presenter

    def execute(self, tag: Optional[str], stop_words: List[str]):
        ads = self._repo.get_by_tag(tag) if tag is not None else self._repo.get_all()
        if stop_words:
            ads = self._exclude_stop_words_from_ads(stop_words, ads)
        last_30_ads = sorted(ads, key=lambda x: x.parse_date, reverse=True)[:30]
        return self._presenter.present(last_30_ads)

    @staticmethod
    def _exclude_stop_words_from_ads(stop_words, ads):
        stop_word_ignore = partial(_stop_word_ignore, stop_words)
        ads = (ad for ad in ads if stop_word_ignore(ad.title))
        ads = (ad for ad in ads if stop_word_ignore(ad.description))
        return ads


def _stop_word_ignore(stop_words: List[str], text: str):
    if not stop_words and not text:
        return True
    # слово или часть слова (слева) начиная с пробела, без учета регистра
    pattern = re.compile('|'.join(rf'\b{word}' for word in stop_words), re.IGNORECASE)
    # match    - "bla" - True - False
    # no match - None  - False - True
    return not bool(pattern.search(text))
