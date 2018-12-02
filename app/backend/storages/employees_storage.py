from sqlalchemy.exc import InvalidRequestError

from domain.exceptions import DbException, InvalidDbQueryException, NotFoundException
from domain.models.employee import Employee


class EmployeesStorage:
    def __init__(self, db):
        self.storage = db

    def save(self, employee):
        self.storage.add(employee)
        self._commit()

    def update(self, employee):
        self.storage.add(employee)
        self._commit()

    def delete(self, entity):
        self.storage.delete(entity)
        self._commit()
        return entity

    def get_all(self):
        return self._find_by().all()

    def find_by_id(self, employee_id):
        employee = self._find_by(id=employee_id).first()
        if not employee:
            raise NotFoundException("employee with {} not found".format(employee_id))
        return employee

    def find_by(self, **kwargs):
        return self._find_by(**kwargs).all()

    def _find_by(self, **kwargs):
        try:
            return self.storage.query(Employee).filter_by(**kwargs)
        except InvalidRequestError as ex:
            raise InvalidDbQueryException(ex)

    def _commit(self):
        try:
            self.storage.commit()
        except Exception as ex:
            self.storage.rollback()
            raise DbException(ex)
