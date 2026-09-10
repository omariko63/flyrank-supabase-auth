from fastapi import APIRouter, Header, HTTPException, status
from supabase_auth.errors import AuthApiError

from app.core.supabase import supabase

router = APIRouter()


@router.get("/profile")
def protected_profile(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"},
        )

    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0] != "Bearer" or not parts[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"},
        )

    token = parts[1]

    try:
        response = supabase.auth.get_user(token)
    except AuthApiError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"},
        )

    user = response.user

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }