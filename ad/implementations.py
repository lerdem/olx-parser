from functools import partial

from ad.adapters.presenter import FeedPresenter, FeedDetailedPresenter
from ad.adapters.repository import GetRepoCsv, GetDetailedRepoCsv
from ad.core.usecases.get_ads import get

get_base = partial(get, repo=GetRepoCsv(), presenter=FeedPresenter())
get_detail = partial(get, repo=GetDetailedRepoCsv(), presenter=FeedDetailedPresenter())
