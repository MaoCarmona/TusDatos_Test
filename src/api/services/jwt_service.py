from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2) }, key=getenv("SECRET"), algorithm="HS256")
    return token


def validate_token(token, output=False):
    """
    Validates a JWT token and returns the decoded token if valid.

    Args:
        token (str): The JWT token to be validated.
        output (bool, optional): If set to True, the function returns the decoded token. Defaults to False.

    Returns:
        dict or None: The decoded token if output is True and the token is valid. None otherwise.

    Raises:
        JSONResponse: If the token is invalid or expired, a JSON response with an appropriate error message and status code is raised.
    """
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"}, status_code=401)