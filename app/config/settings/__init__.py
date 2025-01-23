import os

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import * # noqa
else:
    from .development import * # noqa
