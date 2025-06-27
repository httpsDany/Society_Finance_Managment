from fastapi import FastAPI
from app.auth import auth, oauth
from app.core import management,sync

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(oauth.router, prefix="", tags=["OAuth"])
app.include_router(management.router, prefix="/admin", tags=['Admin Pannel'])
app.include_router(sync.router, prefix="/admin", tags=["Sync"])
