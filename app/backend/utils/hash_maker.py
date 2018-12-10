from passlib.hash import pbkdf2_sha256


class ToHash:
    def __init__(self):
        self.hash_maker = pbkdf2_sha256

    def to_hash(self, origin_data):
        return self.hash_maker.hash(origin_data)

    def check_with_hash(self, origin_data, hashed_data):
        return self.hash_maker.verify(origin_data, hashed_data)
