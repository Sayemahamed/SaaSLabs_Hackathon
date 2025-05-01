# Assuming API is a package/directory at the same level or in sys.path
from API.db import User
from API.schemas import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from API.services import UserService, get_current_user
from fastapi import APIRouter, Depends, status

user_router = APIRouter()


@user_router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a New User",
)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserService = Depends(),
) -> UserResponseSchema:
    """
    Creates a new user account.
    Raises 400 if email already exists.
    """
    # Service handles hashing password and checking for existing email
    user = await user_service.create_user(user_data)
    # Use model_validate for Pydantic v2
    return UserResponseSchema.model_validate(user)


@user_router.put(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update Current User",
)
async def update_user(
    user_update_data: UserUpdateSchema,
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),  # Get the user to update
) -> UserResponseSchema:
    """
    Updates the profile (name, password) of the currently logged-in user.
    """
    updated_user = await user_service.update_user(
        user_to_update=current_user, update_data=user_update_data
    )
    # Use model_validate for Pydantic v2
    return UserResponseSchema.model_validate(updated_user)


@user_router.delete(
    "/", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Current User"
)
async def delete_user(
    user_service: UserService = Depends(),
    current_user: User = Depends(get_current_user),  # Get the user to delete
) -> None:
    """
    Deletes the account of the currently logged-in user.
    """
    await user_service.delete_user(user_to_delete=current_user)
    # No return body for 204
