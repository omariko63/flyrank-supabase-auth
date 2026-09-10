from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.core.supabase import supabase

app = FastAPI(title="FlyRank Supabase Auth")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return {"message": "FlyRank Supabase Auth is running"}

@app.get("/supabase-test")
def supabase_test():
    response = supabase.auth.get_session()

    return {
        "supabase_connected": True,
        "session": response
    }