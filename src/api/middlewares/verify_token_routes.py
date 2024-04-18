from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from services.jwt_service import validate_token

class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()
        
        async def verify_token_middleware(request: Request):
            authorization_header = request.headers.get("Authorization")
            
            if authorization_header is None:
                raise HTTPException(status_code=401, detail="Missing Authorization header")
            
            try:
                token = authorization_header.split(" ")[1]
            except IndexError:
                raise HTTPException(status_code=401, detail="Invalid token format")
            
            validation_response = validate_token(token, output=False)
            if validation_response is None:
                return await original_route(request)
            else:
                raise HTTPException(status_code=401, detail="Invalid token")

        return verify_token_middleware
