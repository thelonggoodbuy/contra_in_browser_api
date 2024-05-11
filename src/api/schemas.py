from ninja import Schema




class User(Schema):
    id: int | None = None
    username: str | None = None
    email: str | None = None



class UserInDB(User):
    hashed_password: str


class Token(Schema):
    access_token: str
    token_type: str


class LoginRequestForm(Schema):
    email: str
    password: str


class ScoreUpdateSchema(Schema):
    value: int