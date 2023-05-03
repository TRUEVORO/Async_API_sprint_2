from http import HTTPStatus

from fastapi import HTTPException


class ServiceError(HTTPException):
    pass


class UnavailableServiceError(ServiceError):
    def __init__(self, detail: str = 'service is unavailable, retry later', **kwargs):
        super().__init__(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=detail, **kwargs)


class NotFoundServiceError(ServiceError):
    def __init__(self, detail: str = 'not found', **kwargs):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail, **kwargs)
