import http

import grpc
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings
from .grpc import user_pb2, user_pb2_grpc


class JWTBearerRemoteGrpc(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Invalid authentication scheme.')
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid token or expired token.')
            return credentials.credentials
        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')

    @staticmethod
    async def verify_jwt(jwt_token: str) -> bool:
        async with grpc.aio.insecure_channel(f'{settings.grpc_host}:{settings.grpc_port}') as channel:
            stub = user_pb2_grpc.DetailerStub(channel)
            request = user_pb2.UserTokenRequest(token=jwt_token)
            try:
                response: user_pb2.UserResponse = await stub.DetailsByToken(request)
                if response is not None:
                    return True
            except grpc.RpcError as e:
                raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail=e.details())
        return False


security_jwt_remote = JWTBearerRemoteGrpc()
