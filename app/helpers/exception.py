

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.helpers import response
from app.helpers.value import is_numeric

# handle 400 Bad Request
async def bad_request(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = str(exception.detail)
    else:
        error = str(exception)

    return response.bad_request(error)

# handle 401 Unauthorized
async def unauthorized(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = str(exception.detail)
    else:
        error = str(exception)

    return response.unauthorized(error)

# handle 403 Forbidden
async def forbidden(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = str(exception.detail)
    else:
        error = str(exception)

    return response.forbidden()

# handle 404 Not Found
async def not_found(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = str(exception.detail)
    else:
        error = str(exception)

    return response.not_found()

# handle 405 Method Not Allowed
async def method_not_allowed(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = exception.detail
    else:
        error = str(exception)

    return response.method_not_allowed()

# handle 422 Validation Error
async def unprocessable_entity(request: Request, exception: RequestValidationError):
    errors = []
    
    for err in exception.errors():
        err_field = []

        for part in err["loc"]:
            if part in ["query", "body"]:
                continue
            elif isinstance(part, int):
                err_field.append(f"[{part}]")
            else:
                err_field.append(str(part))

        errors.append({
            "field": '.'.join(err_field),
            "type": str(err["type"]),
            "message": str(err["msg"])
        })

    return response.unprocessable_entity("Error \"%s\". %s" % (errors[0]["field"], errors[0]["message"]))

# handle 500 Internal Server Error
async def internal_server_error(request: Request, exception: HTTPException):
    if isinstance(exception, HTTPException):
        error = str(exception.detail)
    else:
        error = str(exception)

    return response.internal_server_error(error or None)