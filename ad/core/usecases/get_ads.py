from ad.core.adapters.repository import GetRepo


def get(repo: GetRepo, presenter, tag: str = None):
    ads = repo.get_by_tag(tag) if tag is not None else repo.get_all()
    return presenter.present(ads)
