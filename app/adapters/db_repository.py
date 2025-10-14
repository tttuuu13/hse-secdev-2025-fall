from sqlalchemy.orm import Session

from .. import schemas
from ..domain import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_issues_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Issue)
        .filter(models.Issue.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_issue(db: Session, issue: schemas.IssueCreate, user_id: int):
    db_issue = models.Issue(**issue.model_dump(), owner_id=user_id)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def update_issue(db: Session, issue: models.Issue, issue_update: schemas.IssueUpdate):
    update_data = issue_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(issue, key, value)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def delete_issue(db: Session, issue: models.Issue):
    db.delete(issue)
    db.commit()
