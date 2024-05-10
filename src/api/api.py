from ninja import NinjaAPI

api = NinjaAPI()




@api.get("/get_user_total_score")
def get_user_total_score(request):
    return "you want to get users score!"


@api.post("/post_change_user_total_score")
def change_user_total_score(request):
    return "Change users total score"



# ==========================new====new===========>>>>>>>>>>>>>>>>>>>>>>>>..
from ninja import Schema
from passlib.context import CryptContext
from src.users_app.services.users_service import UserService
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from ninja.errors import AuthenticationError

SECRET_KEY = "e902bbf3a6c28106f91028b01e6158bcab2360acc0676243d70404fe6e731b58"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class User(Schema):
    username: str | None = None
    email: str | None = None



class UserInDB(User):
    hashed_password: str


class Token(Schema):
    access_token: str
    token_type: str



from django.contrib.auth import authenticate


# def verify_password(plain_password, hashed_password):
#     print('---plain_password---')
#     print(plain_password)
#     print('---hashed_password---')
#     print(hashed_password)
#     print('+++++++++++++++++++++')

#     # return pwd_context.verify(plain_password, hashed_password)
#     return authenticate()



async def get_user_and_check_password(email: str, password: str):
    # user = get_user_by_email(db, email)

    user = await UserService.return_user_per_email(email)
    if user and user.check_password(password):
        user_dict = {"hashed_password": user.password, "email": user.email}
        return UserInDB(**user_dict)
    



async def authenticate_user(email: str, password: str):
    user = await get_user_and_check_password(email, password)

    if not user:
        return False
    
    # if not verify_password(password, user.hashed_password):
    #     print('---PASSWORD-IS-NOT-VALIDATED---')
    #     return False
    # if not user.check_password(password):
    #     print('---PASSWORD-IS-NOT-VALIDATED---')
        # return False
    return user



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.now(timezone.utc) + expires_delta
    #     to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    




@api.post("/login")
async def login(request, email: str, password: str):
    user = await authenticate_user(email, password)
    if not user:
        raise AuthenticationError(
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
            data={"sub": user.email}
        )
    # return "you want to login"

    # access_token = create_access_token(
    #         data={"sub": user.email}
    #     )
    
    return Token(access_token=access_token, token_type="bearer")

    