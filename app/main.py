from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from os import listdir, path
import re
from app.config import app as config_app
from app.helpers import exception

app = FastAPI(title=config_app["name"])

# register the exception handlers
app.add_exception_handler(400, exception.bad_request)
app.add_exception_handler(401, exception.unauthorized)
app.add_exception_handler(403, exception.forbidden)
app.add_exception_handler(404, exception.not_found)
app.add_exception_handler(405, exception.method_not_allowed)
app.add_exception_handler(RequestValidationError, exception.unprocessable_entity)
app.add_exception_handler(500, exception.internal_server_error)

# default route
@app.get("/")
async def root():
    return {"message": config_app["name"]}

# register routes
route_path = "./app/routes"
for route in listdir(route_path):
    if path.isfile(path.join(route_path, route)):
        route_name = path.splitext(path.basename(route))[0]
        if re.search("^__.*__$", route_name) == None:
            exec(f"from app.routes import {route_name}")
            app.include_router(eval(f"{route_name}.router"))
