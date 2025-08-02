import logging

from pydantic import BaseModel
from redis import Redis

from url_shortener.config import settings
from url_shortener.exceptions import ShortUrlAlreadyExistsError
from url_shortener.schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

logger = logging.getLogger(__name__)
redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.url_shortener,
)


class ShortUrlStorage(BaseModel):
    hash_name: str

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=self.hash_name,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrl]:
        return [
            ShortUrl.model_validate_json(value) for value in redis.hvals(self.hash_name)
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis.hget(name=self.hash_name, key=slug):
            return ShortUrl.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=self.hash_name,
                key=slug,
            )
        )

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.save_short_url(short_url)
        logger.info("Created short url %s", short_url)
        return short_url

    def create_or_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exists(short_url_in.slug):
            return self.create(short_url_in)

        raise ShortUrlAlreadyExistsError(short_url_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            self.hash_name,
            slug,
        )

    def delete(self, short_url: ShortUrl) -> None:
        logger.info("Deleting short url %s", short_url)
        self.delete_by_slug(short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field, value in short_url_in:
            setattr(short_url, field, value)
        self.save_short_url(short_url)
        logger.info("Updated short url %s", short_url)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field, value)
        self.save_short_url(short_url)
        logger.info("Partial updated short url %s", short_url)
        return short_url


storage = ShortUrlStorage(
    hash_name=settings.redis.collections.url_shortener_hash,
)
