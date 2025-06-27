from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.flat_user import Building, FlatType, FlatTypeMapping, Flat
from app.auth.jwt import require_admin
from sqlalchemy.exc import IntegrityError
from typing import Optional
from ..core.utils import calculate_total_due
from dateutil.relativedelta import relativedelta
    
router = APIRouter()

@router.post("/generate-flats")
def generate_flats(building_no: int, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    mappings = db.query(FlatTypeMapping).filter_by(building_no=building_no).all()
    if not mappings:
        raise HTTPException(status_code=404, detail="No flat mappings found")

    skipped = []
    success = 0

    for mapping in mappings:
        flat_type_cleaned = mapping.flat_type.strip().lower()
        flat_no_cleaned = mapping.flat_no.strip()

        flat_type_obj = db.query(FlatType).filter_by(type_name=flat_type_cleaned).first()
        if not flat_type_obj:
            skipped.append(flat_no_cleaned)
            continue
        new_flat.total_due = calculate_total_due(
        maintenance_fee=flat_type_obj.maintenance_fee,
        due_amt=None,
        fine=0,
        miscellaneous=0
)
        new_flat = Flat(
            building_no=building_no,
            flat_no=flat_no_cleaned,
            flat_type=flat_type_cleaned,
            status="empty",
            maintenance_fee=flat_type_obj.maintenance_fee,
            due_amt=flat_type_obj.rent,  # if applicable
            fine=0,
            miscellaneous=0,
            total_due=None,
            start_date=None,
            due_date=None,
        )

        try:
            db.add(new_flat)
            success += 1
        except IntegrityError:
            db.rollback()
            skipped.append(flat_no_cleaned)

    db.commit()
    return {
        "created_flats": success,
        "skipped_flats": skipped
    }

@router.post("/update-flat-dues")
def update_flat_dues(db: Session = Depends(get_db)):
    today = date.today()
    updated = []

    flats = db.query(Flat).all()

    for flat in flats:
        if not flat.start_date:
            continue

        # Normalize flat_type
        flat_type_cleaned = flat.flat_type.strip().lower() if flat.flat_type else None
        flat_type_obj = db.query(FlatType).filter_by(type_name=flat_type_cleaned).first()
        if not flat_type_obj:
            continue

        # Expected due date = 1 calendar month after start date
        expected_due_date = flat.start_date + relativedelta(months=1)

        # Check if overdue
        if today > expected_due_date:
            fine = (flat.fine or 0) + 50  # Flat fine or use your own logic
            rent = flat_type_obj.rent or 0
            maintenance = flat_type_obj.maintenance_fee or 0
            misc = flat.miscellaneous or 0

            flat.fine = fine
            flat.due_amt = rent
            flat.maintenance_fee = maintenance
            flat.total_due = rent + maintenance + fine + misc
            flat.due_date = expected_due_date

            updated.append(flat.flat_no)

    db.commit()

    return {
        "updated_flats": updated,
        "message": f"Updated {len(updated)} flat(s) with dues/fines"
    }

@router.post("/create-building")
def create_building(
    building_name: str = Form(...),
    floors: int = Form(...),
    flats_per_floor: int = Form(...),
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)
):
    name_cleaned = building_name.strip()

    new_building = Building(
        building_name=name_cleaned,
        floors=floors,
        flats_per_floor=flats_per_floor
    )
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return {"msg": "Building created", "building_no": new_building.building_no}

@router.post("/create-flat-type")
def create_flat_type(
    type_name: str = Form(...),
    maintenance_fee: int = Form(...),
    rent: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)
):
    type_name_cleaned = type_name.strip().lower()

    if db.query(FlatType).filter(FlatType.type_name == type_name_cleaned).first():
        raise HTTPException(status_code=400, detail="Flat type already exists")

    new_type = FlatType(type_name=type_name_cleaned, maintenance_fee=maintenance_fee, rent=rent)
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return {"msg": "Flat type added"}

@router.post("/assign-flat-type", dependencies=[Depends(require_admin)])
def assign_flat_type(
    building_no: int = Form(...),
    flat_no: str = Form(...),
    flat_type: str = Form(...),
    db: Session = Depends(get_db)
):
    flat_type_cleaned = flat_type.strip().lower()
    flat_no_cleaned = flat_no.strip()

    valid_type = db.query(FlatType).filter_by(type_name=flat_type_cleaned).first()
    if not valid_type:
        raise HTTPException(status_code=404, detail="Flat type does not exist")

    existing = db.query(FlatTypeMapping).filter_by(
        building_no=building_no,
        flat_no=flat_no_cleaned
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Mapping already exists")

    mapping = FlatTypeMapping(
        building_no=building_no,
        flat_no=flat_no_cleaned,
        flat_type=flat_type_cleaned
    )

    db.add(mapping)
    db.commit()
    db.refresh(mapping)

    return {"msg": "Flat type mapping created successfully"}

# ------------------ GET ROUTES ------------------ #

@router.get("/buildings", dependencies=[Depends(require_admin)])
def get_all_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()

@router.get("/flat-type-mappings", dependencies=[Depends(require_admin)])
def get_all_flat_type_mappings(db: Session = Depends(get_db)):
    return db.query(FlatTypeMapping).all()

@router.get("/flat-types", dependencies=[Depends(require_admin)])
def get_all_flat_types(db: Session = Depends(get_db)):
    return db.query(FlatType).all()

@router.get("/flats", dependencies=[Depends(require_admin)])
def get_all_flats(db: Session = Depends(get_db)):
    return db.query(Flat).all()

