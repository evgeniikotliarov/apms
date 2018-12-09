import falcon


class BaseError(Exception):
    def get_http_code(self):
        raise NotImplementedError


class AccessDeniedToUpdateTimeSheet(BaseError):
    def get_http_code(self):
        return falcon.HTTP_401


class DbException(BaseError):
    def get_http_code(self):
        return falcon.HTTP_500


class InvalidDbQueryException(BaseError):
    def get_http_code(self):
        return falcon.HTTP_500


class NotFoundException(BaseError):
    def get_http_code(self):
        return falcon.HTTP_404
