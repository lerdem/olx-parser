from functools import partial
import punq

from ad.adapters.presenter import (
    FeedPresenter,
    FeedDetailedPresenter,
    FeedDebugPresenter,
)
from ad.adapters.provider import GetItemProvider, CreateProviderOlx
from ad.adapters.repository import (
    GetRepoCsv,
    GetDetailedRepoCsv,
    DetailRepoCsv,
    CreateRepoCsv,
    ConfigRepoJson,
    GetDebugRepo,
)
from ad.core.adapters.provider import CreateProvider
from ad.core.adapters.repository import CreateRepo, ConfigRepo
from ad.core.usecases.create_base_ads import CreateAdsUseCase
from ad.core.usecases.create_detail_ad import create_detail
from ad.core.usecases.get_ads import get

get_base_ads = partial(get, repo=GetRepoCsv(), presenter=FeedPresenter())
get_detail_ads = partial(
    get, repo=GetDetailedRepoCsv(), presenter=FeedDetailedPresenter()
)
get_full_ads_debug = partial(get, repo=GetDebugRepo(), presenter=FeedDebugPresenter())
ad_detail_uploader = partial(
    create_detail, repository=DetailRepoCsv(), provider=GetItemProvider()
)


container = punq.Container()
container.register(CreateRepo, CreateRepoCsv)
container.register(CreateProvider, CreateProviderOlx)
container.register(ConfigRepo, ConfigRepoJson)
container.register(CreateAdsUseCase)
ads_creator = container.resolve(CreateAdsUseCase)
