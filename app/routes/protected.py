from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter()


@router.get("/profile")
def protected_profile(auth=Depends(get_current_user)):
    user = auth["user"]

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }


@router.get("/dashboard")
def dashboard(auth=Depends(get_current_user)):
    user = auth["user"]

    return {
        "message": "Welcome to your dashboard!",
        "user_id": user.id,
    }