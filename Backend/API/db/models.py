from typing import TYPE_CHECKING

from sqlmodel import Field,  SQLModel

if TYPE_CHECKING:
    pass  # Keep relationships hinting directly for simplicity here, SQLModel handles it well.


class User(SQLModel, table=True):
    """Represents an application user."""

    email: str = Field(primary_key=True, index=True, min_length=5, max_length=255)
    name: str = Field(min_length=3, max_length=100)
    hashed_password: str = Field(nullable=False)
