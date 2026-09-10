import logging

from fastapi import APIRouter, HTTPException, status, Depends, Response
from supabase_auth.errors import AuthApiError

from app.core.supabase import supabase
from app.schemas.auth import AuthRequest
from app.core.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })
    except AuthApiError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": str(e)},
        )

    return response.user


@router.post("/login")
def login(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })
    except AuthApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials"},
        ) from exc
    except Exception as exc:
        logger.exception("Supabase login failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"error": "Authentication service unavailable"},
        ) from exc

    if not response.session:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Email confirmation is required before logging in"},
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(auth=Depends(get_current_user)):
    # sign_out() reads a process-wide stored session. Use the SDK's stateless
    # logout method so this request revokes the token that was actually sent.
    supabase.auth.admin.sign_out(auth["token"])
    return Response(status_code=status.HTTP_204_NO_CONTENT)
