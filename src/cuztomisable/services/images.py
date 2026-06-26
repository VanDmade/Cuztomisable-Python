from sqlalchemy.orm import Session


class ImageService:
    def __init__(self, db: Session):
        self.db = db
