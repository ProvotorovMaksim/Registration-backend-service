from jose import jwt, JWTError
from settings import settings
from datetime import timedelta, datetime

def create_access_token(data: dict):
    dtime: datetime = datetime.utcnow() + timedelta(hours=2)
    to_encode = data.copy()
    to_encode.update({"exp": dtime})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid token")
