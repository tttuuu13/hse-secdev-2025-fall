from sqlalchemy.orm import Session

from .. import schemas
from ..adapters import db_repository
from ..domain import models
from ..shared.errors import ForbiddenError, NotFoundError


class IssueService:
    def __init__(self, db: Session):
        self.db = db

    def create_issue(
        self, issue: schemas.IssueCreate, user: models.User
    ) -> models.Issue:
        return db_repository.create_user_issue(self.db, issue=issue, user_id=user.id)

    def get_issues_by_owner(
        self, user: models.User, skip: int, limit: int
    ) -> list[models.Issue]:
        return db_repository.get_issues_by_owner(
            self.db, owner_id=user.id, skip=skip, limit=limit
        )

    def get_issue_by_id(self, issue_id: int, user: models.User) -> models.Issue:
        db_issue = db_repository.get_issue(self.db, issue_id=issue_id)
        if not db_issue:
            raise NotFoundError("Issue")
        if db_issue.owner_id != user.id and user.role != "admin":
            raise ForbiddenError()
        return db_issue

    def update_issue(
        self, issue_id: int, issue_update: schemas.IssueUpdate, user: models.User
    ) -> models.Issue:
        db_issue = self.get_issue_by_id(issue_id, user)  # Reuse permission check
        return db_repository.update_issue(
            self.db, issue=db_issue, issue_update=issue_update
        )

    def delete_issue(self, issue_id: int, user: models.User):
        db_issue = self.get_issue_by_id(issue_id, user)  # Reuse permission check
        return db_repository.delete_issue(self.db, issue=db_issue)
