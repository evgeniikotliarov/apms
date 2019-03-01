from utils.hash_maker import ToHash


class FakeToHash(ToHash):
    def to_hash(self, origin_data):
        return origin_data

    def check_with_hash(self, origin_data, hashed_data):
        return origin_data == hashed_data
