from os import path
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.helpers.response import ok as send_ok, created as send_created, not_found as send_not_found, bad_request as send_bad_request
from app.helpers.request import filter_data
from app.controllers import app_clients as app_clients_controller
from app.schemas import app_clients as schema

__route = path.splitext(path.basename(__file__))[0]
router = APIRouter(prefix=f"/{__route}", tags=[__route])

@router.get("", response_model=schema.FetchData)
async def fetch_data(query: schema.FetchData = Depends()):
    conditions = filter_data(jsonable_encoder(query))
    result = await app_clients_controller.get_all(conditions)

    if result["total"] > 0:
        return send_ok(**result)

    return send_not_found("Data not found")

@router.post("")
async def insert_data(body: schema.InsertData):
    data = filter_data(jsonable_encoder(body))
    result = await app_clients_controller.insert(data)

    if result["total"] > 0:
        return send_created(**result)

    return send_bad_request(result.get("error") or None)

@router.post("/many")
async def insert_many_data(body: schema.InsertManyData):
    data = filter_data(jsonable_encoder(body))
    result = await app_clients_controller.insert_many(data)

    if result["total"] > 0:
        return send_created(**result)

    return send_bad_request(result.get("error") or None)

@router.post("/many/update")
async def insert_many_update_data(body: schema.InsertManyUpdateData):
    data = filter_data(jsonable_encoder(body))
    result = await app_clients_controller.insert_many_update(data)

    if result["total"] > 0:
        return send_ok(**result)

    return send_bad_request(result.get("error") or None)

@router.get("/{id}")
async def fetch_data_by_id(id: int):
    conditions = dict(id=id)
    result = await app_clients_controller.get_detail(conditions)

    if result["total"] > 0:
        return send_ok(**result)

    if result.get("error"):
        return send_bad_request(result.get("error"))

    return send_not_found("Data not found")

@router.put("/{id}")
async def update_data(id: int, body: schema.UpdateData):
    data = filter_data(jsonable_encoder(body))
    conditions = dict(id=id)
    result = await app_clients_controller.update(data, conditions)

    if result["total"] > 0:
        return send_ok(**result)

    return send_bad_request(result.get("error") or None)

@router.delete("/{id}")
async def delete_data_by_id(id: int):
    conditions = dict(id=id)
    result = await app_clients_controller.delete(conditions)

    if result["total"] > 0:
        return send_ok(**result)

    return send_bad_request(result.get("error") or None)