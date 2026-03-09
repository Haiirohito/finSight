from fastapi import APIRouter
from .services import run_health_checks

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def live():
    return {"status": "alive"}


@router.get("/ready")
def readiness():
    return run_health_checks()
