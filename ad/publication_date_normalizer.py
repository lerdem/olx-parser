from datetime import datetime, timezone

from ad.adapters.repository import DetailedAdRepoSqlite


def normalize_to_utc(dt: datetime) -> datetime:
    """
    Takes a datetime object that is either naive or aware (ZoneInfo/timezone),
    and normalizes it cleanly to a datetime.timezone.utc aware object.
    """
    # If it is offset-naive (like example #2), make it aware by assuming UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
        
    # If it is already aware (ZoneInfo or timezone.utc), 
    # astimezone() will safely convert/normalize its display to timezone.utc
    return dt.astimezone(timezone.utc)

if __name__ == '__main__':
    # prevent TypeError can't compare offset-naive and offset-aware datetimes
    _repo = DetailedAdRepoSqlite()
    for ad in _repo.get_all():
        fixed_dt = normalize_to_utc(ad.publication_date)
        new_ad = ad.copy(update={"publication_date": fixed_dt})
        _repo.save_detail(new_ad)
        print(ad.publication_date, fixed_dt)
    print('dt normalization done')
