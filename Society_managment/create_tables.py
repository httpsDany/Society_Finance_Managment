# create_tables.py

from app.database import Base, engine
from app.models import flat_user  # This imports all models, ensuring they're registered

def create_all_tables():
    print("🔧 Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done: All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
