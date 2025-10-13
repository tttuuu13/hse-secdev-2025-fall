from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="SecDev Course App", version="0.1.0")


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Normalize FastAPI HTTPException into our error envelope
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": detail}},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


# Example minimal entity (for tests/demo)
_DB = {"issues": []}


@app.post("/issues")
def create_issue(title: str):
    if not title or len(title) > 100:
        raise ApiError(
            code="validation_error", message="title must be 1..100 chars", status=422
        )
    issue = {"id": len(_DB["issues"]) + 1, "title": title}
    _DB["issues"].append(issue)
    return issue


@app.get("/issues")
def get_issues():
    return _DB


@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    for it in _DB["issues"]:
        if it["id"] == issue_id:
            return it
    raise ApiError(code="not_found", message="issue not found", status=404)
