from functools import partial

from ad.adapters.presenter import FeedPresenter, FeedDetailedPresenter
from ad.adapters.provider import GetItemProvider, CreateProviderOlx
from ad.adapters.repository import (
    GetRepoCsv,
    GetDetailedRepoCsv,
    DetailRepoCsv,
    CreateRepoCsv,
    ConfigRepoJson,
)
from ad.core.usecases.create_base_ads import create
from ad.core.usecases.create_detail_ad import create_detail
from ad.core.usecases.get_ads import get

get_base = partial(get, repo=GetRepoCsv(), presenter=FeedPresenter())
get_detail = partial(get, repo=GetDetailedRepoCsv(), presenter=FeedDetailedPresenter())
ad_detail_uploader = partial(
    create_detail, repository=DetailRepoCsv(), provider=GetItemProvider()
)
ads_creator = partial(
    create,
    repository=CreateRepoCsv(),
    provider=CreateProviderOlx,
    configuration=ConfigRepoJson(),
)
