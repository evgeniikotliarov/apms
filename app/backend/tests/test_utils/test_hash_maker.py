import unittest

from utils.hash_maker import ToHash


class TestToHashStorage(unittest.TestCase):
    def test_to_hash(self):
        hash_maker = ToHash()
        origin_data = 'some secret data'
        hashed_data = hash_maker.to_hash(origin_data)
        self.assertTrue(hash_maker.check_with_hash(origin_data, hashed_data))

    def test_with_rehashing(self):
        hash_maker = ToHash()
        origin_data = 'some secret data'
        hashed_data = hash_maker.to_hash(origin_data)
        hash_maker.to_hash(origin_data)
        hash_maker.to_hash(origin_data)
        self.assertTrue(hash_maker.check_with_hash(origin_data, hashed_data))
