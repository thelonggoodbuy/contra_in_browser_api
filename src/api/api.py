from ninja import NinjaAPI, Form, Schema, Body, Query
from ninja.errors import AuthenticationError
from .dependencies import authenticate_user, encode_jwt
from .schemas import Token, LoginRequestForm, ScoreUpdateSchema
from .utils.jwt_auth_requied_decorator import jwt_auth_required
from src.users_app.services.users_service import UserService
import json




api = NinjaAPI()






@api.get("/get_user_total_score")
@jwt_auth_required
def get_user_total_score(request) -> int:
    """
    Return users total score of user by token.

    Result:
        - total score (int): total score of concret user
    """

    total_score = UserService.return_score_by_id(request.user.id)

    return_dict = {'user_email': request.user.email, 'total_score': total_score}
    return return_dict


@api.post("/post_change_user_total_score")
@jwt_auth_required
def change_user_total_score(request, data: ScoreUpdateSchema) -> int:
    """
    Change users total score with data received from post request.

    Args:
        - data(ScoreUpdateSchema): json dictionary with value changed in total score.

    Returns:
        - new_total_score(int): new state of total certain user`s score
    """
    updated_score_int = data.value
    new_total_score = UserService.update_score_by_id(request.user.id, updated_score_int)

    return_dict = {'user_email': request.user.email, 'total_score': new_total_score, 'changes_in_score': data.value}
    return return_dict



@api.post("/login")
def login_request(request, form_data: Form[LoginRequestForm]) -> Token:
    """
    Login user and return JWT token.

    Function validate email, check if password is correct
    and return total score
    """
    email = form_data.email
    password = form_data.password
    user = authenticate_user(request, email, password)
    if not user:
        raise AuthenticationError(
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_jwt(user.id)
    return Token(access_token=access_token, token_type="bearer")




