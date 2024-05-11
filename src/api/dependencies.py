from jose import JWTError, jwt
from src.users_app.services.users_service import UserService
from .schemas import UserInDB


SECRET_KEY = "e902bbf3a6c28106f91028b01e6158bcab2360acc0676243d70404fe6e731b58"
ALGORITHM = "HS256"



def encode_jwt(payload):
    payload = {"user_id": payload}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
