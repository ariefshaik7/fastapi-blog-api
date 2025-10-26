from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password) -> bool:
    """
    verifies a plain text password against a hashed apssword.
    """
    return pwd_context.verify(plain_password, hashed_password)