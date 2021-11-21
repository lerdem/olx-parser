import punq

from ad.adapters.presenter import BaseAdFeedPresenter, DetailedAdFeedPresenter
from ad.adapters.provider import DetailedAdProviderOlx, CreateProviderOlx
from ad.adapters.repository import (
    GetBaseAdRepoCsv,
    DetailedAdGetRepoCsv,
    DetailedAdRepoCsv,
    CreateAdsRepoCsv,
    CreateAdsConfigJson,
)
from ad.core.adapters import Presenter
from ad.core.adapters.provider import CreateAdsProvider, DetailedAdProvider
from ad.core.adapters.repository import (
    CreateAdsRepo,
    CreateAdsConfig,
    DetailedAdRepo,
    GetRepo,
)
from ad.core.usecases.create_base_ads import CreateAdsUseCase
from ad.core.usecases.create_detail_ad import CreateDetailedAdUseCase
from ad.core.usecases.get_ads import GetAdsUseCase

container = punq.Container()
container.register(CreateAdsRepo, CreateAdsRepoCsv)
container.register(CreateAdsProvider, CreateProviderOlx)
container.register(CreateAdsConfig, CreateAdsConfigJson)
container.register(CreateAdsUseCase)
ads_creator = container.resolve(CreateAdsUseCase)

container.register(DetailedAdRepo, DetailedAdRepoCsv)
container.register(DetailedAdProvider, DetailedAdProviderOlx)
container.register(CreateDetailedAdUseCase)
ad_detail_uploader = container.resolve(CreateDetailedAdUseCase)


container.register(GetRepo, DetailedAdGetRepoCsv)
container.register(Presenter, DetailedAdFeedPresenter)
container.register(GetAdsUseCase)
get_detail_ads = container.resolve(GetAdsUseCase)

container2 = punq.Container()
container2.register(GetRepo, GetBaseAdRepoCsv)
container2.register(Presenter, BaseAdFeedPresenter)
container2.register(GetAdsUseCase)
get_base_ads = container2.resolve(GetAdsUseCase)
