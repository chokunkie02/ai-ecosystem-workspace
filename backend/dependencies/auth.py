from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Mocking JWT token validation
    if token != "valid-token": # Replace with actual validation logic
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "mock_user"
