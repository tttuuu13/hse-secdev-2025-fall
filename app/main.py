from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bug Lite",
    version="0.1.0",
    description="A simplified bug tracker.",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/issues/", response_model=schemas.Issue)
def create_issue_for_user(
    user_id: int, issue: schemas.IssueCreate, db: Session = Depends(get_db)
):
    return crud.create_user_issue(db=db, issue=issue, user_id=user_id)


@app.get("/issues/", response_model=List[schemas.Issue])
def read_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    issues = crud.get_issues(db, skip=skip, limit=limit)
    return issues
