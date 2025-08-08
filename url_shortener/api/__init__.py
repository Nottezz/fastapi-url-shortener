from fastapi import APIRouter

from .short_urls.views import router as short_urls_router  # type: ignore [attr-defined]

router = APIRouter(prefix="/api")
router.include_router(short_urls_router)
