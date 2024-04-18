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
    """
    Handles a POST request to the `/login` endpoint.

    Args:
        user (User): The user object containing the username and email.

    Returns:
        Union[str, JSONResponse]: If the username is "Mauricio Carmona", returns a token as a string.
        If the username is not found, returns a JSON response with a "User not found" message and a 404 status code.
    """
    if user.username == "Mauricio Carmona":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)


@auth_router.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    """
    Validates a JWT token extracted from the Authorization header.

    Args:
        Authorization (str): The value of the Authorization header in the format "Bearer <token>".

    Returns:
        Union[dict, JSONResponse]: If the token is valid and successfully decoded, the decoded token is returned.
                                   If the token is invalid or expired, a JSONResponse with a status code of 401 and
                                   an appropriate error message is returned.
    """
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)