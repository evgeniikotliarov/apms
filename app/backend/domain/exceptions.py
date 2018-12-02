class AccessDeniedToUpdateTimeSheet(Exception):
    pass


class DbException(Exception):
    pass


class InvalidDbQueryException(Exception):
    pass


class NotFoundException(Exception):
    pass
