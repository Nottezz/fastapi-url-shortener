from fastapi import APIRouter

from .main_view import router as main_router
from .short_urls import router as short_urls

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_router)
router.include_router(short_urls)
