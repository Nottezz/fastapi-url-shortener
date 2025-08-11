from pydantic import AnyHttpUrl, BaseModel, Field


class ShortUrlBase(BaseModel):
    """
    Base model for short url
    """

    target_url: AnyHttpUrl
    summary: str = Field(
        "",
        min_length=10,
        max_length=100,
        title="URL summary",
    )


class ShortUrlCreate(ShortUrlBase):
    """
    Model for create short url
    """

    slug: str = Field(
        ...,
        min_length=3,
        max_length=10,
        title="URL slug",
    )
    summary: str | None = Field(  # type: ignore[assignment]
        None,
        min_length=10,
        max_length=100,
        title="URL summary",
    )


class ShortUrlUpdate(ShortUrlBase):
    """
    Model for updating a short url
    """


class ShortUrlPartialUpdate(BaseModel):
    """
    Model for partial updating a short url
    """

    target_url: AnyHttpUrl | None = None
    summary: str | None = Field(
        None,
        min_length=10,
        max_length=100,
        title="URL summary",
    )


class ShortUrlRead(ShortUrlBase):
    """
    Model for reading a short url
    """

    slug: str = Field(
        ...,
        min_length=3,
        max_length=10,
        title="URL slug",
    )
    summary: str | None = Field(  # type: ignore[assignment]
        None,
        min_length=10,
        max_length=100,
        title="URL summary",
    )


class ShortUrl(ShortUrlBase):
    """
    Model for short url
    """

    slug: str = Field(
        ...,
        min_length=3,
        max_length=10,
        title="URL slug",
    )
    summary: str | None = Field(  # type: ignore[assignment]
        None,
        min_length=10,
        max_length=100,
        title="URL summary",
    )
