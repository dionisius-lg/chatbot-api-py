from os import path
from app.utils.database import Database
from datetime import datetime
import json

__table = path.splitext(path.basename(__file__))[0]

async def get_all(conditions: dict = None):
    custom_conditions = []

    if isinstance(conditions, dict) and conditions.get("name"):
        custom_conditions.append(f"{__table}.name LIKE '%{conditions['name']}%'")
        del conditions["name"]

    if isinstance(conditions, dict) and conditions.get("start"):
        start = datetime.fromtimestamp(conditions["start"]).strftime('%Y-%m-%d')
        end = start

        if isinstance(conditions, dict) and conditions.get("end"):
            end = datetime.fromtimestamp(conditions["end"]).strftime('%Y-%m-%d')
            del conditions["end"]

        custom_conditions.append(f"(DATE {__table}.created_at BETWEEN '{start}' AND '{end}')")

    column_select = []

    column_deselect = []

    custom_columns = [
        "IFNULL(created_users.fullname, created_users.username) AS created_user",
        "IFNULL(updated_users.fullname, updated_users.username) AS updated_user"
    ]

    join = [
        f"LEFT JOIN users AS created_users ON created_users.id = {__table}.created_by",
        f"LEFT JOIN users AS updated_users ON updated_users.id = {__table}.updated_by"
    ]

    group_by = []

    custom_orders = []

    having = []

    result = Database().get_list_data(
        table=__table,
        conditions=conditions,
        custom_conditions=custom_conditions,
        column_select=column_select,
        column_deselect=column_deselect,
        custom_columns=custom_columns,
        join=join,
        group_by=group_by,
        custom_orders=custom_orders,
        having=having
    )

    if result.get("data"):
        for i, _ in enumerate(result["data"]):
            if result["data"][i].get("auth"):
                try:
                    result["data"][i]["auth"] = json.loads(result["data"][i]["auth"])
                except Exception as err:
                    # do nothing
                    pass

    return result

async def get_detail(conditions: dict = None):
    custom_conditions = []

    if isinstance(conditions, dict) and conditions.get("name"):
        custom_conditions.append(f"{__table}.name LIKE '%{conditions['name']}%'")
        del conditions["name"]

    if isinstance(conditions, dict) and conditions.get("start"):
        start = datetime.fromtimestamp(conditions["start"]).strftime('%Y-%m-%d')
        end = start

        if isinstance(conditions, dict) and conditions.get("end"):
            end = datetime.fromtimestamp(conditions["end"]).strftime('%Y-%m-%d')
            del conditions["end"]

        custom_conditions.append(f"(DATE {__table}.created_at BETWEEN '{start}' AND '{end}')")

    column_select = []

    column_deselect = []

    custom_columns = [
        "IFNULL(created_users.fullname, created_users.username) AS created_user",
        "IFNULL(updated_users.fullname, updated_users.username) AS updated_user"
    ]

    join = [
        f"LEFT JOIN users AS created_users ON created_users.id = {__table}.created_by",
        f"LEFT JOIN users AS updated_users ON updated_users.id = {__table}.updated_by"
    ]

    group_by = []

    result = Database().get_row_data(
        table=__table,
        conditions=conditions,
        custom_conditions=custom_conditions,
        column_select=column_select,
        column_deselect=column_deselect,
        custom_columns=custom_columns,
        join=join,
        group_by=group_by
    )

    if result.get("data"):
        for key in result["data"]:
            if key in ["auth"]:
                try:
                    result["data"][key] = json.loads(result["data"][key])
                except Exception as err:
                    # do nothing
                    pass


    return result

async def insert(data: dict):
    protected_columns = ["id"]

    if data.get("auth") and isinstance(data["auth"], dict):
        data = dict(data, auth=json.dumps(data["auth"]))

    result = Database().insert_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def insert_many(data: list):
    protected_columns = ["id"]

    for i, _ in enumerate(data):
        if data[i].get("auth") and isinstance(data[i]["auth"], dict):
            data[i] = dict(data[i], auth=json.dumps(data[i]["auth"]))

    result = Database().insert_many_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def insert_many_update(data: list):
    protected_columns = []

    for i, _ in enumerate(data):
        if data[i].get("auth") and isinstance(data[i]["auth"], dict):
            data[i] = dict(data[i], auth=json.dumps(data[i]["auth"]))

    result = Database().insert_many_update_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def update(data: dict, conditions: dict):
    protected_columns = ["id"]

    if data.get("auth") and isinstance(data["auth"], dict):
        data = dict(data, auth=json.dumps(data["auth"]))

    result = Database().update_data(
        table=__table,
        data=data,
        conditions=conditions,
        protected_columns=protected_columns
    )

    return result

async def delete(conditions: dict):
    result = Database().delete_data(
        table=__table,
        conditions=conditions
    )

    return result