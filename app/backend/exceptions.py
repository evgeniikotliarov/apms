import falcon


class BaseError(Exception):
    def get_http_code(self):
        raise NotImplementedError


class AccessDeniedToUpdateTimeSheetError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_401


class DbError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_500


class InvalidDbQueryError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_500


class NotFoundError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_404


class EmailIsBusyError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_400


class AuthenticationError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_401


class InvalidTokenError(BaseError):
    pass


class TokenExpiredError(BaseError):
    pass
