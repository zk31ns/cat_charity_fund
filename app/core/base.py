"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base
from app.models.user import User
from app.models.charity_project import CharityProject
from app.models.donation import Donation

__all__ = [
    'Base',
    'User',
    'CharityProject',
    'Donation',
]
