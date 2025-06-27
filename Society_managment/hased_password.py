from passlib.context import CryptContext

# Use same hashing context as your FastAPI app
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Replace with your password
plain_password = "danyal"

# Generate the hashed password
hashed_password = pwd_context.hash(plain_password)

print("Hashed password:", hashed_password)

