from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBaseSchema(BaseModel):
    """Base schema for user attributes."""

    email: EmailStr = Field(..., description="User's email address (unique identifier)")
    name: str = Field(..., min_length=3, max_length=100, description="User's full name")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Convert email to lowercase."""
        return v.lower()


class UserCreateSchema(UserBaseSchema):
    """Schema for creating a new user."""

    password: str = Field(
        ..., min_length=8, description="User's password (min 8 characters)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "john.doe@example.com",
                    "name": "John Doe",
                    "password": "aSecurePassword123",
                }
            ]
        }
    )


class UserUpdateSchema(BaseModel):
    """Schema for updating an existing user. All fields are optional."""

    name: Optional[str] = Field(
        None, min_length=3, max_length=100, description="New full name for the user"
    )
    password: Optional[str] = Field(
        None, min_length=8, description="New password (min 8 characters)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "Johnny Doe"},
                {"password": "anotherSecurePassword456"},
                {"name": "Johnathan Doe", "password": "newPassword789"},
            ]
        }
    )


class UserResponseSchema(UserBaseSchema):
    """Schema for returning user information (excluding password)."""

    # Inherits email and name from UserBaseSchema

    # Pydantic V2 configuration - enables creating schema from ORM model
    model_config = ConfigDict(from_attributes=True)
