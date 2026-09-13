from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.routes.auth import router as auth_router
from app.core.supabase import supabase
from app.routes.public import router as public_router
from app.routes.protected import router as protected_router
from app.routes.quiz import router as quiz_router
from app.exceptions.handlers import validation_exception_handler

app = FastAPI(title="FlyRank Supabase Auth")
app.include_router(auth_router, prefix="/auth")
app.include_router(public_router, prefix="/public")
app.include_router(protected_router, prefix="/protected")
app.include_router(quiz_router, prefix="/quiz")

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

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