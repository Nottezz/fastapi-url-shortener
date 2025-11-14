from fastapi import APIRouter, HTTPException, status

from storage.short_url.crud import storage
from url_shortener.exceptions import ShortUrlAlreadyExistsError
from url_shortener.schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

router = APIRouter(
    prefix="/shortener",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def get_short_url_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A short url with such slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL with slug <name> already exists.",
                    },
                },
            },
        },
    },
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    try:
        return storage.create_or_raise_if_exists(short_url_create)
    except ShortUrlAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug <{short_url_create.slug}> already exists.",
        )
