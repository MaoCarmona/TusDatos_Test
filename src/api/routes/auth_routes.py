from fastapi import APIRouter, Header
from pydantic import BaseModel, EmailStr
from services.jwt_service import validate_token, write_token
from fastapi.responses import JSONResponse

auth_router = APIRouter()

class User(BaseModel):
    username: str
    email: EmailStr

@auth_router.post("/login")
def login(user: User):
    if user.username == "Mauricio Carmona":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@auth_router.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)