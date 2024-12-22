from os import path
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.helpers import response
from app.helpers.value import filter_data
from app.controllers import users as controller
from app.schemas import users as schema

__route = path.splitext(path.basename(__file__))[0]
router = APIRouter(prefix=f"/{__route}", tags=[__route])

@router.get("", response_model=schema.FetchData)
async def fetch_data(query: schema.FetchData = Depends()):
    conditions = filter_data(jsonable_encoder(query))
    result = await controller.get_all(conditions)

    if result["total"] > 0:
        return response.ok(**result)

    return response.not_found_data()

@router.post("")
async def insert_data(body: schema.InsertData):
    data = filter_data(jsonable_encoder(body))
    result = await controller.insert(data)

    if result["total"] > 0:
        return response.created(**result)

    return response.bad_request(result.get("error") or None)

@router.post("/many")
async def insert_many_data(body: schema.InsertManyData):
    data = filter_data(jsonable_encoder(body))
    result = await controller.insert_many(data)

    if result["total"] > 0:
        return response.created(**result)

    return response.bad_request(result.get("error") or None)

@router.post("/many/update")
async def insert_many_update_data(body: schema.InsertManyData):
    data = filter_data(jsonable_encoder(body))
    result = await controller.insert_many_update(data)

    if result["total"] > 0:
        return response.ok(**result)

    return response.bad_request(result.get("error") or None)

@router.get("/{id}")
async def fetch_data_by_id(id: int):
    conditions = dict(id=id)
    result = await controller.get_detail(conditions)

    if result["total"] > 0:
        return response.ok(**result)

    if result.get("error"):
        return response.bad_request(result.get("error"))

    return response.not_found_data()

@router.put("/{id}")
async def update_data(id: int, body: schema.UpdateData):
    data = filter_data(jsonable_encoder(body))
    conditions = dict(id=id)
    result = await controller.update(data, conditions)

    if result["total"] > 0:
        return response.ok(**result)

    return response.bad_request(result.get("error") or None)

@router.delete("/{id}")
async def delete_data_by_id(id: int):
    conditions = dict(id=id)
    result = await controller.delete(conditions)

    if result["total"] > 0:
        return response.ok(**result)

    return response.bad_request(result.get("error") or None)