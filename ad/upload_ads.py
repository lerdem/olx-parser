from functools import partial


from ad.adapters.provider import CreateProviderOlx
from ad.adapters.repository import CreateRepoCsv, ConfigRepoJson
from ad.core.usecases.create_base_ads import create
from ad.adapters.provider import GetItemProvider
from ad.adapters.repository import DetailRepoCsv
from ad.core.usecases.create_detail_ad import create_detail

detail_uploader = partial(
    create_detail, repository=DetailRepoCsv(), provider=GetItemProvider()
)

if __name__ == '__main__':
    new_ad_ids = create(CreateRepoCsv(), CreateProviderOlx(), ConfigRepoJson())
    print(new_ad_ids)
    for _id in new_ad_ids:
        detail_uploader(ad_id=_id)
