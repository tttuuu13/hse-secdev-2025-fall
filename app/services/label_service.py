from sqlalchemy.orm import Session

from .. import schemas
from ..domain import models


class LabelService:
    def __init__(self, db: Session):
        self.db = db

    def create_label(self, label: schemas.LabelCreate) -> models.Label:
        return models.Label(id=999, name=label.name)
