from passlib.context import CryptContext

# Setting default hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# defining a function to hash the password
def hash(password: str):
    return pwd_context.hash(password)


# comparing the hashed password with the password at login
def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)
