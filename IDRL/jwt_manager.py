import jwt
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request

def create_token(data: dict) -> str:
    token: str = jwt.encode(data, 'secret', algorithm='HS256')
    return token

def validate_token(token: str) -> dict:
    try:
        data : dict = jwt.decode(token, 'secret', algorithms=['HS256'])
        return data
    except:
        return None
    
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data is None:
            raise HTTPException(status_code=401, detail='Credenciales inválidas')