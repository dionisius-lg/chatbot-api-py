from fastapi.responses import JSONResponse
from math import ceil
from typing import Any

# response 200 OK
def ok(total:int = 0, data: list[dict[str, Any]] | dict[str, Any] = None, limit: int | None = None, page: int | None = None):
    result = {
        "success": True,
        "total": total,
        "data": data or {}
    }

    if isinstance(limit, int) and isinstance(page, int):
        if limit > 0 and total > 0:
            page_current = page
            page_next = page + 1
            page_previous = page - 1
            page_first = 1
            page_last = ceil(total / limit)

            result["paging"] = {
                "current": page_current,
                "next": page_next if page_next <= page_last else page_current,
                "previous": page_previous if page_previous > 0 else 1,
                "first": page_first,
                "last": page_last if page_last > 0 else 1
            }

    return JSONResponse(status_code=200, content=result)

# response 201 Created
def created(total:int = 0, data: list|dict = None):
    result = {
        "success": True,
        "total": total,
        "data": data or {}
    }

    return JSONResponse(status_code=201, content=result)

# response 400 Bad Request
def bad_request(message:str = None):
    result = {
        "success": False,
        "title": "Bad Request",
        "message": message or "Request is invalid"
    }

    return JSONResponse(status_code=400, content=result)

# response 401 Unauthorized
def unauthorized(message:str = None):
    result = {
        "success": False,
        "title": "Unauthorized",
        "message": message or "You do not have rights to access this resource"
    }

    return JSONResponse(status_code=401, content=result)

# response 403 Forbidden
def forbidden(message:str = None):
    result = {
        "success": False,
        "title": "Forbidden",
        "message": message or "You do not have rights to access this resource"
    }

    return JSONResponse(status_code=403, content=result)

# response 404 Not Found
def not_found(message:str = None):
    result = {
        "success": False,
        "title": "Not Found",
        "message": message or "Resource not found"
    }

    return JSONResponse(status_code=404, content=result)

# response 405 Method Not Allowed
def method_not_allowed(message:str = None):
    result = {
        "success": False,
        "title": "Method Not Allowed",
        "message": message or "This resource is not match with your request method"
    }

    return JSONResponse(status_code=405, content=result)

# response 422 Validation Error
def unprocessable_entity(message:str = None):
    result = {
        "success": False,
        "title": "Unprocessable Entity",
        "message": message or "Unprocessable entity"
    }

    return JSONResponse(status_code=422, content=result)

# response 429 Too Many Requests
def too_many_request(message:str = None):
    result = {
        "success": False,
        "title": "Too Many Requests",
        "message": message or "Too many requests"
    }

    return JSONResponse(status_code=429, content=result)

# response 500 Internal Server Error
def internal_server_error(message:str = None):
    result = {
        "success": False,
        "title": "Internal Server Error",
        "message": message or "The server encountered an error, please try again later"
    }

    return JSONResponse(status_code=500, content=result)