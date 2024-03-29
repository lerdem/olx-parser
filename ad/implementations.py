import punq

from ad.adapters.presenter import DetailedAdFeedPresenter
from ad.adapters.provider import DetailedAdProviderOlx, CreateProviderOlx
from ad.adapters.repository import (
    DetailedAdGetRepoCsv,
    DetailedAdRepoCsv,
    CreateAdsRepoCsv,
    CreateAdsConfigJson,
    GetDebugRepo,
)
from ad.core.adapters import Presenter
from ad.core.adapters.provider import CreateAdsProvider, DetailedAdProvider
from ad.core.adapters.repository import (
    CreateAdsRepo,
    CreateAdsConfig,
    DetailedAdRepo,
    GetDetailedAdRepo,
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

container.register(GetDetailedAdRepo, DetailedAdGetRepoCsv)
container.register(Presenter, DetailedAdFeedPresenter)
container.register(GetAdsUseCase)
_get_ads_usecase = container.resolve(GetAdsUseCase)
get_detail_ads = _get_ads_usecase.execute

container3 = punq.Container()
container3.register(GetDetailedAdRepo, GetDebugRepo)
container3.register(Presenter, DetailedAdFeedPresenter)
container3.register(GetAdsUseCase)
_get_ads_debug_usecase = container3.resolve(GetAdsUseCase)
get_full_ads_debug = _get_ads_debug_usecase.execute
