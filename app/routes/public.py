from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/info", status_code=status.HTTP_200_OK)
def public():
    return {
        "message" : "Welcome stranger! This info is public."
    }
