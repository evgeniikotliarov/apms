from sqlalchemy.exc import InvalidRequestError

from exceptions import DbError, InvalidDbQueryError, NotFoundError


class Storage:
    def __init__(self, db, type_cls):
        self.storage = db
        self.type = type_cls

    def save(self, entity):
        self.storage.add(entity)
        self._commit()

    def update(self, entity):
        self.storage.add(entity)
        self._commit()

    def delete(self, entity):
        self.storage.delete(entity)
        self._commit()
        return entity

    def get_all(self):
        return self._find_by().all()

    def find_by_id(self, entity_id):
        entity = self._find_by(id=entity_id).first()
        if not entity:
            message = "{} with id {} not found".format(self.type.__name__, entity_id)
            raise NotFoundError(message)
        return entity

    def find_first_by(self, **kwargs):
        entity = self._find_by(**kwargs).first()
        if not entity:
            args_list = map(lambda value: str(value), kwargs.values())
            arguments = ', '.join(args_list)
            raise NotFoundError("{} with id {} not found".format(self.type.__name__, arguments))
        return entity

    def find_by(self, **kwargs):
        return self._find_by(**kwargs).all()

    def _find_by(self, **kwargs):
        try:
            return self.storage.query(self.type).filter_by(**kwargs)
        except InvalidRequestError as ex:
            raise InvalidDbQueryError(ex)

    def _commit(self):
        try:
            self.storage.commit()
        except Exception as ex:
            self.storage.rollback()
            raise DbError(ex)
