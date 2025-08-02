class ShortUrlBaseError(Exception):
    """
    Base exception for short url
    """


class ShortUrlAlreadyExistsError(ShortUrlBaseError):
    """
    Raised when a short url already exists
    """
