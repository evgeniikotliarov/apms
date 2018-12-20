from datetime import timedelta, datetime

import jwt as jwt
from jwt import DecodeError

from exceptions import InvalidTokenError, TokenExpiredError
from utils.to_num_converter import ToNum


class Tokenizer:
    days_for_expire = 7
    secret = "secret_word"
    algorithm = 'HS256'

    def get_data_by_token(self, raw_token, date=datetime.today()):
        token = self.__get_parsed_token(raw_token)
        origin_data = self._decode_token(token)
        self.__validate_expired_date(origin_data, date)
        return origin_data

    def get_token_by_data(self, origin_data, date=datetime.today()):
        exp_date = date + timedelta(days=self.days_for_expire)
        origin_data['exp_date'] = "{}-{}-{}".format(exp_date.year, exp_date.month, exp_date.day)
        return self._encode_token(origin_data)

    def _encode_token(self, origin_data):
        token = jwt.encode(origin_data, self.secret, algorithm=self.algorithm)
        return token.decode("utf-8")

    def _decode_token(self, token):
        try:
            decode = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return decode
        except DecodeError:
            raise InvalidTokenError()

    @classmethod
    def __get_parsed_token(cls, token):
        try:
            if ' ' in token:
                bearer, token = token.split(' ')
            if not token:
                raise InvalidTokenError()
            return token
        except ValueError:
            raise InvalidTokenError()

    @classmethod
    def __validate_expired_date(cls, credentials, date):
        exp_date_year, exp_date_month, exp_date_day = credentials['exp_date'].split('-')
        converter = ToNum()
        expired_date = datetime(
            converter.to_num(exp_date_year),
            converter.to_num(exp_date_month),
            converter.to_num(exp_date_day))
        if expired_date <= date:
            raise TokenExpiredError()
