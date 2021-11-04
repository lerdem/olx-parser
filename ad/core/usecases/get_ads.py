from ad.core.adapters.repository import GetRepo


def get(repo: GetRepo, presenter):
    return presenter.present(repo.get_all())
