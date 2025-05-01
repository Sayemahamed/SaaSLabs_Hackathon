from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    """Schema for the response containing the access token."""

    access_token: str
    token_type: str

    # Pydantic V2 configuration
    model_config = ConfigDict(from_attributes=True)
