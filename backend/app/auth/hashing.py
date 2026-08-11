from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
_MAX_BCRYPT_BYTES = 72


def _truncate_to_bcrypt_limit(password: str) -> str:
    b = password.encode("utf-8")
    print("truncating", b)
    print(len(b), "bytes")
    if len(b) <= _MAX_BCRYPT_BYTES:
        return password
    truncated = b[:_MAX_BCRYPT_BYTES]
    return truncated.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    pw = _truncate_to_bcrypt_limit(plain_password)
    return pwd_context.verify(pw, password_hash)
