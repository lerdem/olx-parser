class EntityError(Exception):
    pass


class UseCaseError(EntityError):
    pass


class AdapterError(EntityError):
    pass
