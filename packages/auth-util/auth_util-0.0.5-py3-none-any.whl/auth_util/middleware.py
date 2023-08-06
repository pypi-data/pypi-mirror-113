import jwt
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send

from auth_util import JwtManager


class JwtMiddleware:
    """Validate jwt and add user to scope"""
    not_validate_suffix = ['docs', 'openapi.json', 'login', 'register']
    jwt_manager = JwtManager()
    jwt_header = 'jwt'
    jwt_payload_key = 'payload'
    jwt_key = 'jwt'

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # prepare data
        request = Request(scope, receive=receive)

        if request.method == 'OPTIONS':
            pass
        else:
            path = request.url.path[1:].split('/')
            if path[-1] in self.not_validate_suffix:
                pass
            else:
                token = request.headers.get(self.jwt_header, '')
                if token:
                    try:
                        payload = self.jwt_manager.decode_jwt(token)
                        scope[self.jwt_payload_key] = payload
                        scope[self.jwt_key] = token
                    except jwt.exceptions.DecodeError:
                        raise HTTPException(status_code=401, detail='jwt decode error')
                    except jwt.exceptions.ExpiredSignatureError:
                        raise HTTPException(status_code=401, detail='jwt expired')
                else:
                    raise HTTPException(status_code=401, detail='without jwt')
        await self.app(scope, receive, send)
