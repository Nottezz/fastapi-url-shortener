from fastapi import APIRouter

from .list_view import router as list_view

router = APIRouter(
    prefix="/shortener",
    tags=["URL Shortener"],
)
router.include_router(list_view)
