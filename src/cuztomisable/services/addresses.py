import uuid

from sqlalchemy.orm import Session


class AddressService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_id(self, address_id: uuid.UUID):
        pass

    def create(self, user_id: uuid.UUID, data: dict):
        pass

    def update(self, address_id: uuid.UUID, data: dict):
        pass

    def delete(self, address_id: uuid.UUID):
        pass
