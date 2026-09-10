from fastapi import APIRouter, HTTPException, status
from supabase_auth.errors import AuthApiError

from app.core.supabase import supabase
from app.schemas.auth import AuthRequest

router = APIRouter()


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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials"},
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
    }