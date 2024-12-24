import sys
import os
import re
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.config import app as config_app
from app.helpers import exception

# add main app dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI(title=config_app["name"])

# add exception handlers
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
for route in os.listdir(route_path):
    if os.path.isfile(os.path.join(route_path, route)):
        route_name = os.path.splitext(os.path.basename(route))[0]
        if re.search("^__.*__$", route_name) == None:
            exec(f"from app.routes import {route_name}")
            app.include_router(eval(f"{route_name}.router"))

# run with command: python -m app.main
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(config_app["port"]), reload=config_app["reload"])