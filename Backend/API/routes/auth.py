# Assuming API is a package/directory at the same level or in sys.path
from API.schemas import TokenResponse
from API.services import AuthService, create_access_token, verify_password
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()


@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),  # Use Depends() directly if AuthService has dependencies
) -> TokenResponse:
    """
    Authenticates a user and returns an access token.
    Uses OAuth2PasswordRequestForm, expecting 'username' (mapped to email) and 'password'.
    """
    user = await auth_service.get_user_by_email(email=form_data.username.lower())

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(access_token=access_token, token_type="bearer")
