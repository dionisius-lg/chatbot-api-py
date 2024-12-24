from os import path
from app.utils.database import Database
from datetime import datetime

__table = path.splitext(path.basename(__file__))[0]

async def get_all(conditions: dict = None):
    custom_conditions = []

    if isinstance(conditions, dict) and conditions.get("pattern"):
        custom_conditions.append(f"{__table}.pattern LIKE '%{conditions['pattern']}%'")
        del conditions["pattern"]

    if isinstance(conditions, dict) and conditions.get("tag"):
        custom_conditions.append(f"intents.tag LIKE '%{conditions['tag']}%'")
        del conditions["tag"]

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
        "IFNULL(updated_users.fullname, updated_users.username) AS updated_user",
        "intents.tag"
    ]

    join = [
        f"LEFT JOIN users AS created_users ON created_users.id = {__table}.created_by",
        f"LEFT JOIN users AS updated_users ON updated_users.id = {__table}.updated_by",
        f"LEFT JOIN intents ON intents.id = {__table}.intent_id"
    ]

    group_by = [f"{__table}.id"]

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

    return result

async def get_detail(conditions: dict = None):
    custom_conditions = []

    if isinstance(conditions, dict) and conditions.get("tag"):
        custom_conditions.append(f"{__table}.tag LIKE '%{conditions['tag']}%'")
        del conditions["tag"]

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
        "IFNULL(updated_users.fullname, updated_users.username) AS updated_user",
        "intents.tag"
    ]

    join = [
        f"LEFT JOIN users AS created_users ON created_users.id = {__table}.created_by",
        f"LEFT JOIN users AS updated_users ON updated_users.id = {__table}.updated_by",
        f"LEFT JOIN intents ON intents.id = {__table}.intent_id"
    ]

    group_by = [f"{__table}.id"]

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

    return result

async def insert(data: dict):
    protected_columns = ["id"]

    result = Database().insert_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def insert_many(data: list):
    protected_columns = ["id"]

    result = Database().insert_many_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def insert_many_update(data: list):
    protected_columns = []

    result = Database().insert_many_update_data(
        table=__table,
        data=data,
        protected_columns=protected_columns
    )

    return result

async def update(data: dict, conditions: dict):
    protected_columns = ["id"]

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