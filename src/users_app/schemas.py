from ninja import Schema




class CheckTokenModel(Schema):
    user_id: int | None = None
    text_error: str | None = None




class CreateRoomSchema(Schema):
    user_id: int | None = None
    text_error: str | None = None
    room_token: str | None = None
