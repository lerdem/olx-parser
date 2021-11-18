from functools import partial
import punq

from ad.adapters.presenter import FeedPresenter, FeedDetailedPresenter
from ad.adapters.provider import GetItemProvider, CreateProviderOlx
from ad.adapters.repository import (
    GetRepoCsv,
    GetDetailedRepoCsv,
    DetailRepoCsv,
    CreateRepoCsv,
    ConfigRepoJson,
)
from ad.core.adapters.provider import CreateProvider, DetailProvider
from ad.core.adapters.repository import CreateRepo, ConfigRepo, DetailRepo
from ad.core.usecases.create_base_ads import CreateAdsUseCase
from ad.core.usecases.create_detail_ad import CreateDetailUseCase
from ad.core.usecases.get_ads import get

get_base_ads = partial(get, repo=GetRepoCsv(), presenter=FeedPresenter())
get_detail_ads = partial(
    get, repo=GetDetailedRepoCsv(), presenter=FeedDetailedPresenter()
)


container = punq.Container()
container.register(CreateRepo, CreateRepoCsv)
container.register(CreateProvider, CreateProviderOlx)
container.register(ConfigRepo, ConfigRepoJson)
container.register(CreateAdsUseCase)
ads_creator = container.resolve(CreateAdsUseCase)


container.register(DetailRepo, DetailRepoCsv)
container.register(DetailProvider, GetItemProvider)
container.register(CreateDetailUseCase)
ad_detail_uploader = container.resolve(CreateDetailUseCase)
