from fastapi import FastAPI
from app.auth import auth, oauth
from app.core import management,sync
from app.database import Base, engine
from app.models import flat_user


app = FastAPI()

# Automatically create tables in the database on startup (safe if tables already exist)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(oauth.router, prefix="", tags=["OAuth"])
app.include_router(management.router, prefix="/admin", tags=['Admin Pannel'])
app.include_router(sync.router, prefix="/admin", tags=["Sync"])
