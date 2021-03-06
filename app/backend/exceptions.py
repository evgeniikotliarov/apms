import falcon


class BaseError(Exception):
    def get_http_code(self):
        raise NotImplementedError


class AccessDeniedToUpdateTimeSheetError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_403


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
        return '400 Email is busy'


class AuthenticationError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_401


class DeactivatedEmployeeError(BaseError):
    def get_http_code(self):
        return '403 User is deactivated'


class AuthorizationError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_403


class InvalidTokenError(BaseError):
    def get_http_code(self):
        return falcon.HTTP_401


class TokenExpiredError(BaseError):
    def get_http_code(self):
        return '401 Token expired'


class UpdatingError(BaseError):
    def get_http_code(self):
        return '400 Update error'
