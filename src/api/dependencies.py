from jose import JWTError, jwt
from src.users_app.services.users_service import UserService
from .schemas import UserInDB
import os


JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


def encode_jwt(payload):
    payload = {"user_id": payload}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
    

def get_user_and_check_password(request, email: str, password: str):
    user = UserService.return_user_per_email(email)
    if user and user.check_password(password):
        user_dict = {"hashed_password": user.password, "email": user.email, "id": user.id, "username": user.username}
        return UserInDB(**user_dict)
    



def authenticate_user(request, email: str, password: str):
    user = get_user_and_check_password(request, email, password)
    if not user:
        return False
    return user
