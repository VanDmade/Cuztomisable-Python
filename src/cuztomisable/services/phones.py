import uuid

from sqlalchemy.orm import Session

from cuztomisable.db.models.phone import Phone


class PhoneService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_id(self, phone_id: uuid.UUID):
        pass

    def create(self, user_id: uuid.UUID, data: dict) -> Phone:
        phone = Phone(user_id=user_id, **data)
        self.db.add(phone)
        self.db.commit()
        self.db.refresh(phone)
        return phone

    def update(self, phone_id: uuid.UUID, data: dict):
        pass

    def delete(self, phone_id: uuid.UUID):
        pass
