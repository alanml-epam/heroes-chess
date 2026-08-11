from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, password_hash)
