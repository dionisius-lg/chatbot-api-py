import os
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from app.helpers.response import ok as send_ok, not_found as send_not_found, internal_server_error as send_internal_server_error
from app.helpers.request import filter_data
from app.helpers.excel import export as excel_export
from app.helpers.encryption import encrypt
from app.controllers import intents as intents_controller
from app.controllers import patterns as patterns_controller
from app.schemas import intents as intents_schema
from app.schemas import patterns as patterns_schema

__route = os.path.splitext(os.path.basename(__file__))[0]
router = APIRouter(prefix=f"/{__route}", tags=[__route])

# initialize a thread pool executor
executor = ThreadPoolExecutor(max_workers=2)

@router.get("/intents")
async def export_intents(request: Request, query: intents_schema.FetchData = Depends()):
    host = request.headers.get("host")
    protocol = request.url.scheme
    conditions = filter_data(jsonable_encoder(query))
    result = await intents_controller.get_all(conditions)

    if result["total"] > 0:
        column_data = {
            "tag": "Tag",
            "is_active": "Is Active",
            "created_at": "Created At",
            "created_user": "Created By",
            "updated_at": "Created At",
            "updated_user": "Updated By"
        }

        row_data = result["data"]

        excel = await asyncio.to_thread(excel_export, column_data, row_data, file_name="report-intents", sub_path="export")
        destination = excel.pop("destination")
        encrypted = encrypt(json.dumps(excel, separators=(',', ':')))

        if encrypted is None:
            return send_internal_server_error()

        link = f"{protocol}://{host}/files/{encrypted}"

        return send_ok(total=1, data=dict(link=link))

    return send_not_found("Data not found")

@router.get("/patterns")
async def export_patterns(request: Request, query: patterns_schema.FetchData = Depends()):
    host = request.headers.get("host")
    protocol = request.url.scheme
    conditions = filter_data(jsonable_encoder(query))
    result = await patterns_controller.get_all(conditions)

    if result["total"] > 0:
        column_data = {
            "tag": "Tag",
            "is_active": "Is Active",
            "created_at": "Created At",
            "created_user": "Created By",
            "updated_at": "Created At",
            "updated_user": "Updated By"
        }

        row_data = result["data"]

        excel = await asyncio.to_thread(excel_export, column_data, row_data, file_name="report-intents", sub_path="export")
        destination = excel.pop("destination")
        encrypted = encrypt(json.dumps(excel, separators=(',', ':')))

        if encrypted is None:
            return send_internal_server_error()

        link = f"{protocol}://{host}/files/{encrypted}"

        return send_ok(total=1, data=dict(link=link))

    return send_not_found("Data not found")