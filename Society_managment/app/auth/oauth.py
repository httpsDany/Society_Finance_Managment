from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import os

from ..database import get_db
from ..models.flat_user import User
from .jwt import create_access_token

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo") or await oauth.google.parse_id_token(request, token)
    email = user_info.get("email")
    name = user_info.get("name")

    # Check if user already exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, username=name, role="resident")  # Default to resident
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_access_token({"sub": email, "role": user.role})
    return {"access_token": jwt_token, "token_type": "bearer", "role": user.role}

