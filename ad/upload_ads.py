from ad.implementations import ad_detail_uploader, ads_creator

if __name__ == '__main__':
    new_ad_ids = ads_creator()
    print(new_ad_ids)
    for _id in new_ad_ids:
        ad_detail_uploader(ad_id=_id)
