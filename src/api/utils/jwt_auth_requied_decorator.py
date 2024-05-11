from functools import wraps
from src.api.dependencies import decode_jwt
from asgiref.sync import async_to_sync
from src.users_app.services.users_service import UserService



def jwt_auth_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid authorization header"}
        token = auth_header.split()[1]
        payload = decode_jwt(token)
        user = UserService.return_user_by_id(id=int(payload['user_id']))
        request.user = user
        if not payload:
            return {"error": "Invalid JWT token"}


        return func(request, *args, **kwargs)

    return wrapper

