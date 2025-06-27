from fastapi import APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from ..database import get_db
from app.models.flat_user import User, Flat
from .hashing import hash_password, verify_password
from .jwt import create_access_token
from .jwt import require_admin
from typing import Optional
from ..core.utils import calculate_total_due

router = APIRouter()

@router.post("/signup")
def signup(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    building_no: int = Form(...),
    floor_no: int = Form(...),
    flat_no: str = Form(...),
    role: str = Form(...),  # owner or renter
    start_date: Optional[str] = Form(None),  # format: YYYY-MM-DD
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)
):
    # --------- Normalize Inputs ---------
    email = email.strip().lower()
    username = username.strip()
    role = role.strip().lower()
    flat_no = str(flat_no).strip()
    full_flat_no = f"{floor_no:02d}{flat_no.zfill(2)}"  # Pad flat no if needed

    # --------- Validate role ---------
    if role not in ["owner", "renter"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'owner' or 'renter'.")

    # --------- Validate start_date format ---------
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Start date must be in YYYY-MM-DD format")

    # --------- Check for duplicate email ---------
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # --------- Check flat mapping exists ---------
    mapping = db.query(FlatTypeMapping).filter_by(
        building_no=building_no,
        flat_no=full_flat_no
    ).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Flat not assigned a type. Please map it first.")

    # --------- Check flat exists ---------
    flat = db.query(Flat).filter_by(
        building_no=building_no,
        flat_no=full_flat_no
    ).first()
    if not flat:
        raise HTTPException(status_code=404, detail="Flat not found. Please generate it first.")

    # --------- Check if flat already assigned to a user ---------
    if db.query(User).filter(
        User.flat_building_no == building_no,
        User.flat_no == full_flat_no
    ).first():
        raise HTTPException(status_code=409, detail="This flat is already assigned to another user.")

    # --------- Update flat with status & start date ---------
    flat.status = role  # owner or renter
    flat.start_date = start_date

    # --------- Create user ---------
    new_user = User(
        email=email,
        username=username,
        password_hash=hash_password(password),
        role=role,
        flat_building_no=building_no,
        flat_no=full_flat_no,
        building_no=building_no
    )

    db.add_all([new_user, flat])
    db.commit()
    db.refresh(new_user)
    
    flat = db.query(Flat).filter(
        Flat.building_no == building_no,
        Flat.flat_no == flat_str
    ).first()

    if flat:
        flat.status = "owned" if new_user.role == "admin" else "rented"
        flat.start_date = start_date
        flat.total_due = calculate_total_due(
            maintenance_fee=flat.maintenance_fee,
            due_amt=flat.due_amt,
            fine=flat.fine,
            miscellaneous=flat.miscellaneous
        )
        db.commit()


    return {"msg": f"User '{username}' assigned to flat {full_flat_no} in building {building_no}"}


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
