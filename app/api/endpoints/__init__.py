# app/api/endpoints/__init__.py
from .user import router as user_router # noqa
from .charity_project import router as charity_project_router # noqa
from .donation import router as donation_router # noqa


__all__ = [
    'user_router',
    'charity_project_router',
    'donation_router',
]