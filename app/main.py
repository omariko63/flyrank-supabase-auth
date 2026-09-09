from fastapi import FastAPI

from app.core.supabase import supabase

app = FastAPI(title="FlyRank Supabase Auth")


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