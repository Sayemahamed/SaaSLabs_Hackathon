import logging

# Assuming API is a package/directory at the same level or in sys.path
from API.db import User, get_async_session
from API.schemas import UserCreateSchema, UserUpdateSchema

# Import password hashing utilities from auth_service
from API.services import get_password_hash
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

logger = logging.getLogger(__name__)


class UserService:
    """Handles business logic related to user CRUD operations."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Helper to find a user by email."""
        statement = select(User).where(User.email == email.lower())
        result = await self.session.exec(statement)
        return result.first()

    async def create_user(self, user_data: UserCreateSchema) -> User:
        """
        Creates a new user in the database.

        Raises:
            HTTPException(400) if email already exists.
            HTTPException(500) for database errors.
        """
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(
                f"Attempt to create user with existing email: {user_data.email}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,  # Already normalized by schema
            name=user_data.name,
            hashed_password=hashed_password,
        )

        self.session.add(new_user)
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
            logger.info(f"Successfully created user: {new_user.email}")
            return new_user
        except (
            IntegrityError
        ) as e:  # Catch potential race conditions or other integrity issues
            await self.session.rollback()
            logger.error(
                f"IntegrityError creating user {user_data.email}: {e}", exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create user due to a database conflict.",
            )
        except Exception as e:
            await self.session.rollback()
            logger.error(
                f"Unexpected error creating user {user_data.email}: {e}", exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating the user.",
            )

    async def update_user(
        self, user_to_update: User, update_data: UserUpdateSchema
    ) -> User:
        """
        Updates an existing user's information (name and/or password).

        Raises:
            HTTPException(500) for database errors.
        """
        update_dict = update_data.model_dump(
            exclude_unset=True
        )  # Get only provided fields
        updated = False

        if not update_dict:
            # No fields provided for update
            return user_to_update  # Return the user as is

        for key, value in update_dict.items():
            if key == "password":
                setattr(user_to_update, "hashed_password", get_password_hash(value))
                updated = True
            elif hasattr(user_to_update, key):
                setattr(user_to_update, key, value)
                updated = True

        if not updated:
            return user_to_update  # Should not happen if update_dict is not empty

        self.session.add(user_to_update)  # Add the modified user object to the session
        try:
            await self.session.commit()
            await self.session.refresh(user_to_update)
            logger.info(f"Successfully updated user: {user_to_update.email}")
            return user_to_update
        except Exception as e:  # Catch potential errors during commit/refresh
            await self.session.rollback()
            logger.error(
                f"Error updating user {user_to_update.email}: {e}", exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while updating the user.",
            )

    async def delete_user(self, user_to_delete: User) -> None:
        """
        Deletes a user from the database.

        Raises:
            HTTPException(500) for database errors.
        """
        email_to_delete = (
            user_to_delete.email
        )  # Store email for logging before deletion
        try:
            await self.session.delete(user_to_delete)
            await self.session.commit()
            logger.info(f"Successfully deleted user: {email_to_delete}")
        except Exception as e:  # Catch potential errors during delete/commit
            await self.session.rollback()
            logger.error(f"Error deleting user {email_to_delete}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while deleting the user.",
            )
