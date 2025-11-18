from fastapi import APIRouter

from .create_view import router as create_view
from .list_view import router as list_view
from .update_view import router as update_view

router = APIRouter(
    prefix="/shortener",
    tags=["URL Shortener"],
)
router.include_router(list_view)
router.include_router(create_view)
router.include_router(update_view)
