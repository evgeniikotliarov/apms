from sqlalchemy.exc import InvalidRequestError

from exceptions import DbException, InvalidDbQueryException, NotFoundException


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
            raise NotFoundException("{} with id {} not found".format(self.type.__name__, entity_id))
        return entity

    def find_by(self, **kwargs):
        return self._find_by(**kwargs).all()

    def _find_by(self, **kwargs):
        try:
            return self.storage.query(self.type).filter_by(**kwargs)
        except InvalidRequestError as ex:
            raise InvalidDbQueryException(ex)

    def _commit(self):
        try:
            self.storage.commit()
        except Exception as ex:
            self.storage.rollback()
            raise DbException(ex)