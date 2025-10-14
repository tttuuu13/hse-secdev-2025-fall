from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

from . import schemas
from .adapters import db_repository
from .database import Base, engine, get_db
from .domain import models
from .limiter import limiter
from .services.issue_service import IssueService
from .services.user_service import UserService
from .shared.errors import AppError, ConflictError, ForbiddenError, NotFoundError

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bug Lite",
    version="0.1.0",
    description="A simplified bug tracker.",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


router = APIRouter(prefix="/api/v1")


# Exception Handler
@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    status_code = 400
    if isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, ForbiddenError):
        status_code = 403
    elif isinstance(exc, ConflictError):
        status_code = 409

    return JSONResponse(
        status_code=status_code,
        content={"code": exc.code, "message": exc.message},
    )


# Dependencies
def get_current_user(
    x_user_id: Optional[int] = Header(None), db: Session = Depends(get_db)
) -> models.User:
    """Gets user from DB based on X-User-Id header."""
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header missing")
    user = db_repository.get_user(db, user_id=x_user_id)
    if user is None:
        raise NotFoundError("User")
    return user


def get_issue_service(db: Session = Depends(get_db)) -> IssueService:
    return IssueService(db)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


# Endpoints
@router.post("/users/", response_model=schemas.User)
@limiter.limit("10/minute")
def create_user(
    request: Request,
    user: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(user)


@router.post("/issues/", response_model=schemas.Issue)
def create_issue(
    issue: schemas.IssueCreate,
    current_user: models.User = Depends(get_current_user),
    issue_service: IssueService = Depends(get_issue_service),
):
    return issue_service.create_issue(issue, current_user)


@router.get("/issues/", response_model=List[schemas.Issue])
def read_issues(
    current_user: models.User = Depends(get_current_user),
    issue_service: IssueService = Depends(get_issue_service),
    skip: int = 0,
    limit: int = 100,
):
    return issue_service.get_issues_by_owner(current_user, skip, limit)


@router.get("/issues/{issue_id}", response_model=schemas.Issue)
def read_issue(
    issue_id: int,
    current_user: models.User = Depends(get_current_user),
    issue_service: IssueService = Depends(get_issue_service),
):
    return issue_service.get_issue_by_id(issue_id, current_user)


@router.patch("/issues/{issue_id}", response_model=schemas.Issue)
def update_issue(
    issue_id: int,
    issue_update: schemas.IssueUpdate,
    current_user: models.User = Depends(get_current_user),
    issue_service: IssueService = Depends(get_issue_service),
):
    return issue_service.update_issue(issue_id, issue_update, current_user)


@router.delete("/issues/{issue_id}", status_code=204)
def delete_issue(
    issue_id: int,
    current_user: models.User = Depends(get_current_user),
    issue_service: IssueService = Depends(get_issue_service),
):
    issue_service.delete_issue(issue_id, current_user)
    return


app.include_router(router)
