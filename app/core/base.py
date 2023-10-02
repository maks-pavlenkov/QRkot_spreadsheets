"""Импорты класса Base и всех моделей для Alembic."""
from app.models.charity_project import CharityProject  # noqa
from app.models.donation import Donation  # noqa
from app.models.user import User  # noqa
from .db import Base  # noqa
