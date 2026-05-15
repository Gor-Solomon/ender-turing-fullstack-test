from typing import Any
from fastapi import APIRouter, Depends
from app.api.deps import RequireManager

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get(
    "/",
    dependencies=[Depends(RequireManager)],
)
def read_metrics() -> Any:
    """
    Retrieve dummy metrics.
    """
    return {"status": "ok", "data": "dummy data"}
