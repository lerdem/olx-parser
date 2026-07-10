import os
import punq

from ad.adapters.presenter import (
    DetailedAdFeedPresenter,
    DetailedAdDashboardPresenter,
)
from ad.adapters.provider import (
    DetailedAdProviderOlx,
    CreateProviderOlx,
    AvalabilityProviderOlx,
)
from ad.adapters.repository import (
    DetailedAdRepoSqlite,
    CreateAdsRepoSqlite,
    CreateAdsConfigJson,
    GetDebugRepo,
    GetTableDebugRepo,
    NTFYPusher,
)
from ad.core.adapters import Presenter
from ad.core.adapters.provider import (
    CreateAdsProvider,
    DetailedAdProvider,
    AvalabilityProvider,
)
from ad.core.adapters.repository import (
    CreateAdsRepo,
    CreateAdsConfig,
    DetailedAdRepo,
    GetDetailedAdRepo,
    Sender,
)
from ad.core.usecases.create_base_ads import (
    CreateAdsUseCase,
    CreateBaseAdsAndNotificateUC,
)
from ad.core.usecases.create_detail_ad import (
    CreateDetailedAdUseCase,
    UploadDetailedAdsUseCase,
    DeactivationDetailedAdsUseCase,
)
from ad.core.usecases.get_ads import GetAdsUseCase

IS_DEBUG = os.getenv("APP_ENV", "production").lower() == "debug"

container = punq.Container()


if IS_DEBUG:
    container.register(GetDetailedAdRepo, GetDebugRepo)
    print('DEGUG enabled')
else:
    container.register(GetDetailedAdRepo, DetailedAdRepoSqlite)

# REPOS
container.register(CreateAdsRepo, CreateAdsRepoSqlite)
container.register(DetailedAdRepo, DetailedAdRepoSqlite)
container.register(CreateAdsConfig, CreateAdsConfigJson)
container.register(Sender, NTFYPusher)

#PROVIDERS
container.register(CreateAdsProvider, CreateProviderOlx)
container.register(DetailedAdProvider, DetailedAdProviderOlx)
container.register(AvalabilityProvider, AvalabilityProviderOlx)

# #PRESENTERS
container.register(DetailedAdFeedPresenter)
container.register(DetailedAdDashboardPresenter)
_shared_repo = container.resolve(GetDetailedAdRepo)
_feed_presenter = container.resolve(DetailedAdFeedPresenter)
_dashboard_presenter = container.resolve(DetailedAdDashboardPresenter)

container.register(CreateAdsUseCase)
ads_creator = container.resolve(CreateAdsUseCase)

container.register(CreateBaseAdsAndNotificateUC)
create_ads_and_notify = container.resolve(CreateBaseAdsAndNotificateUC)

container.register(CreateDetailedAdUseCase)
ad_detail_uploader = container.resolve(CreateDetailedAdUseCase)

container.register(UploadDetailedAdsUseCase)
_upload_detailed_ads = container.resolve(UploadDetailedAdsUseCase)
bulk_update_missed_detail_ads = _upload_detailed_ads

container.register(DeactivationDetailedAdsUseCase)
bulk_ads_deactivation = container.resolve(DeactivationDetailedAdsUseCase)


_feed_usecase = GetAdsUseCase(
    _repo=_shared_repo,
    _presenter=_feed_presenter,
)
get_detail_ads = _feed_usecase.execute

_get_ads_debug_usecase = GetAdsUseCase(
    _repo=_shared_repo,
    _presenter=_feed_presenter,
)
get_full_ads_debug = _get_ads_debug_usecase.execute

_dashboard_usecase = GetAdsUseCase(
    _repo=_shared_repo,
    _presenter=_dashboard_presenter,
)
get_dashboard_detail_ads = _dashboard_usecase.execute
