from url_shortener.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": settings.logging.log_format,
            "datefmt": settings.logging.log_date_format,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["default"],
        "level": settings.logging.log_level,
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": settings.logging.log_level,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": settings.logging.log_level,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": settings.logging.log_level,
            "propagate": False,
        },
    },
}
