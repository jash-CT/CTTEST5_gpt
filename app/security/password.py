from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Using Argon2 for secure password hashing. Parameters can be tuned for deployment.
ph = PasswordHasher()


def hash_password(plain: str) -> str:
    return ph.hash(plain)


def verify_password(hash: str, plain: str) -> bool:
    try:
        return ph.verify(hash, plain)
    except VerifyMismatchError:
        return False
