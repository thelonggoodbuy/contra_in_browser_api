from src.users_app.models import CustomUser
from asgiref.sync import sync_to_async
# from src.api.dependencies import decode_jwt
import jwt
from src.users_app.schemas import CreateRoomSchema
from datetime import datetime, timedelta, timezone

SECRET_KEY = "e902bbf3a6c28106f91028b01e6158bcab2360acc0676243d70404fe6e731b58"
ALGORITHM = "HS256"





class UserService():

    @classmethod
    def return_score_by_id(cls, id: int) -> int:
        user = CustomUser.objects.get(id=id)
        return user.total_score
    
    @classmethod
    def update_score_by_id(cls, id: int, updated_score_value: int) -> int:
        user = cls.return_user_by_id(id)
        user.total_score += updated_score_value
        user.save()
        return user.total_score

    @classmethod
    def return_user_per_email(cls, email: str):
        user_obj = CustomUser.objects.get(email=email)
        return user_obj
    
    @classmethod
    def return_user_by_id(cls, id: int):
        user_obj = CustomUser.objects.get(id=id)
        return user_obj
    


    @classmethod
    def check_if_token_is_correct(cls, token: str) -> CreateRoomSchema:

        try:
            access_token = token.split()[1]
        except AttributeError:
            # return {"id": None, "error": "You need to login"}
            return CreateRoomSchema(**{"user_id": None, 
                                       "text_error": "You need to login"})
        
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.exceptions.DecodeError:
             return CreateRoomSchema(**{"user_id": None, 
                                       "text_error": "Error in token. Please relogin"})

        if not payload:
            return CreateRoomSchema(**{"user_id": None, "text_error": 
                                       "Error in token. Please relogin"})
    
        else:
            # user = UserService.return_user_by_id(id=int(payload['user_id']))
            user = UserService.return_user_by_id(id=int(payload['user_id']))
            room_token = UserService.generate_enter_the_room_token(user.id)
            return CreateRoomSchema(**{"user_id": user.id, "room_token": room_token})



    @classmethod
    def generate_enter_the_room_token(cls, user_id: int) -> str:
        to_encode = {'user_id': user_id, 'datetime': str(datetime.now(timezone.utc))}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

