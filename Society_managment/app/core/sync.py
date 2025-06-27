from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import timedelta, date

from app.database import get_db
from app.models.flat_user import Flat, FlatTypeMapping, FlatType, User
from app.auth.jwt import require_admin

router = APIRouter()

@router.post("/sync-flats", dependencies=[Depends(require_admin)])
def sync_flats(db: Session = Depends(get_db)):
    # STEP 1: Sync mappings into flats
    mappings = db.query(FlatTypeMapping).all()
    for mapping in mappings:
        flat_type_obj = db.query(FlatType).filter_by(type_name=mapping.flat_type).first()
        if not flat_type_obj:
            continue

        flat = db.query(Flat).filter_by(
            building_no=mapping.building_no,
            flat_no=mapping.flat_no
        ).first()

        if not flat:
            flat = Flat(
                building_no=mapping.building_no,
                flat_no=mapping.flat_no,
                flat_type=mapping.flat_type,
                status="empty",
                maintenance_fee=flat_type_obj.maintenance_fee,
                fine=0,
                miscellaneous=0,
                total_due=flat_type_obj.maintenance_fee
            )
            db.add(flat)
        else:
            flat.flat_type = mapping.flat_type
            flat.maintenance_fee = flat_type_obj.maintenance_fee

    db.commit()

    # STEP 2: Sync users into flats
    users = db.query(User).filter(User.role != "resident").all()
    for user in users:
        flat = db.query(Flat).filter_by(
            building_no=user.flat_building_no,
            flat_no=user.flat_no
        ).first()

        if flat:
            flat.status = "owned" if user.role in ("admin", "owner") else "rented"
            flat.start_date = flat.start_date or date.today()
            flat.due_date = flat.start_date + timedelta(days=30)
            flat.due_amt = 0 if flat.status == "owned" else 10000  # change logic as needed
            flat.total_due = (
                (flat.maintenance_fee or 0)
                + (flat.due_amt or 0)
                + (flat.fine or 0)
                + (flat.miscellaneous or 0)
            )

    db.commit()
    return {"message": "Flats synced successfully."}

