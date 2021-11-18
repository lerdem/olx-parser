import punq

from ad.adapters.presenter import FeedPresenter, FeedDetailedPresenter
from ad.adapters.provider import DetailProviderOlx, CreateProviderOlx
from ad.adapters.repository import (
    GetRepoCsv,
    GetDetailedRepoCsv,
    DetailRepoCsv,
    CreateRepoCsv,
    ConfigRepoJson,
)
from ad.core.adapters import Presenter
from ad.core.adapters.provider import CreateProvider, DetailProvider
from ad.core.adapters.repository import CreateRepo, ConfigRepo, DetailRepo, GetRepo
from ad.core.usecases.create_base_ads import CreateAdsUseCase
from ad.core.usecases.create_detail_ad import CreateDetailUseCase
from ad.core.usecases.get_ads import GetAdsUseCase

container = punq.Container()
container.register(CreateRepo, CreateRepoCsv)
container.register(CreateProvider, CreateProviderOlx)
container.register(ConfigRepo, ConfigRepoJson)
container.register(CreateAdsUseCase)
ads_creator = container.resolve(CreateAdsUseCase)

container.register(DetailRepo, DetailRepoCsv)
container.register(DetailProvider, DetailProviderOlx)
container.register(CreateDetailUseCase)
ad_detail_uploader = container.resolve(CreateDetailUseCase)


container.register(GetRepo, GetDetailedRepoCsv)
container.register(Presenter, FeedDetailedPresenter)
container.register(GetAdsUseCase)
get_detail_ads = container.resolve(GetAdsUseCase)

container2 = punq.Container()
container2.register(GetRepo, GetRepoCsv)
container2.register(Presenter, FeedPresenter)
container2.register(GetAdsUseCase)
get_base_ads = container2.resolve(GetAdsUseCase)
