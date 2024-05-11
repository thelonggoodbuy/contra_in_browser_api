from src.users_app.models import CustomUser
from asgiref.sync import sync_to_async



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
    
