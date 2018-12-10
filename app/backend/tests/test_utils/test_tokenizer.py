import unittest
from datetime import datetime

from exceptions import TokenExpiredError, InvalidTokenError
from utils.tokenizer import Tokenizer


class TestTokenizerStorage(unittest.TestCase):
    def test_tokenizer(self):
        tokenizer = Tokenizer()
        origin_data = {
            'some_key': 'some_value',
            'additional_key': 'additional_value'
        }
        token = tokenizer.get_token_by_data(origin_data)
        self.assertIsNotNone(token)
        data_from_token = tokenizer.get_data_by_token(token)
        self.assertEqual(origin_data, data_from_token)

    def test_tokenizer_with_bearer(self):
        tokenizer = Tokenizer()
        origin_data = {
            'some_key': 'some_value',
            'additional_key': 'additional_value'
        }
        token = tokenizer.get_token_by_data(origin_data)
        self.assertIsNotNone(token)
        data_from_token = tokenizer.get_data_by_token('Bearer ' + token)
        self.assertEqual(origin_data, data_from_token)

    def test_expired_token(self):
        tokenizer = Tokenizer()
        origin_data = {
            'some_key': 'some_value',
            'additional_key': 'additional_value'
        }
        token = tokenizer.get_token_by_data(origin_data, datetime(2018, 1, 1))
        try:
            tokenizer.get_data_by_token(token, datetime(2018, 1, 8))
            raise Exception('token must be expired')
        except TokenExpiredError:
            pass

    def test_with_invalid_token(self):
        tokenizer = Tokenizer()
        try:
            tokenizer.get_data_by_token('invalid_token')
            raise Exception("Invalid token can't get an origin data")
        except InvalidTokenError:
            pass
