import json

from sqlalchemy.types import String, TypeDecorator


class ArrayType(TypeDecorator):
    @property
    def python_type(self):
        return ArrayType

    def process_literal_param(self, value, dialect):
        pass

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        # noinspection PyUnresolvedReferences
        return ArrayType(self.impl.length)
