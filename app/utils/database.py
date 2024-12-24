from mysql.connector import pooling
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date, time
from app.config import database as config
from app.helpers.value import is_empty, is_numeric, escape
from app.helpers.request import filter_column_data
import re

class Database:
    def __init__(self):
        for key in config:
            exec(f"self.{key} = '{config[key]}'")

    def __connect(self):
        try:
            conf = self.__dict__
            pool = pooling.MySQLConnectionPool(
                pool_name="apipool",
                pool_size=5,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
                autocommit=True,
                raw=True,
                **conf
            )

            return pool.get_connection()
        except Exception as err:
            print("Error while connecting to MySQL using Connection pool ", err.msg)
            return {"err": err.__dict__}

    def __check_column(
            self,
            table: str
        ) -> List[str]:
        result = []
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{config['database']}' AND TABLE_NAME = '{table}'"

        conn = self.__connect()

        if not conn.is_connected():
            return result
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)

            data = [dict((cursor.column_names[i], v.decode("utf8") if isinstance(v, (bytes, bytearray)) else v) for i, v in enumerate(row)) for row in cursor.fetchall()]

            for row in data:
                result.append(row["COLUMN_NAME"])

            conn.close()
        except Exception as err:
            print("Error while run function __check_column ", err.msg)

        return result

    def __check_column_detail(
            self,
            table: str
        ) -> Dict[str, Any]:
        result = {}

        query = f"SELECT COLUMN_NAME, COLUMN_KEY, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{config['database']}' AND TABLE_NAME = '{table}'"

        conn = self.__connect()

        if not conn.is_connected():
            return result

        try:
            cursor = conn.cursor()
            cursor.execute(query)

            data = [dict((cursor.column_names[i], v.decode("utf8") if isinstance(v, (bytes, bytearray)) else v) for i, v in enumerate(row)) for row in cursor.fetchall()]

            for row in data:
                result[row["COLUMN_NAME"]] = {
                    "type": row["DATA_TYPE"],
                    "key": row["COLUMN_KEY"],
                    "nullable": row["IS_NULLABLE"]
                }

            conn.close()
        except Exception as err:
            print("Error while run function __check_column_deatail ", err.msg)

        return result

    def count_data(
            self,
            table: str,
            conditions: Optional[dict] = None,
            custom_conditions: Optional[List[str]] = None,
            join: Optional[List[str]] = None,
            group_by: Optional[List[str]] = None,
            having: Optional[List[str]] = None,
        ) -> dict :
        result = {
            "total": 0
        }

        conn = self.__connect()

        if not conn.is_connected() or not table:
            return result

        master_columns = self.__check_column(table)
        query = f"SELECT COUNT(*) AS count FROM {table}"
        condition_query = []
        count_query = ''

        if join and isinstance(join, list):
            join_query = ' '.join(join)
            query += f" {join_query}"

        if conditions and isinstance(conditions, dict):
            for key in conditions:
                if isinstance(conditions[key], list):
                    condition_query.append(f"{table}.{key} IN ({', '.join(map(escape, conditions[key]))})")
                else:
                    condition_query.append(f"{table}.{key} = {escape(conditions[key])}")

        if custom_conditions and isinstance(custom_conditions, list):
            condition_query.extend(custom_conditions)

        if not is_empty(condition_query):
            condition_query = ' AND '.join(condition_query)
            query += f" WHERE {condition_query}"

        if group_by and isinstance(group_by, list):
            # strip each group column
            group_query = list(col.strip() for col in group_by)
            # add prefix table when group column in master columns
            group_query = list(f"{table}.{col}" if col in master_columns else col for col in group_query)
            # join group column
            group_query = ", ".join(group_query)

            query += f" GROUP BY {group_query}"

            if having and isinstance(having, list):
                having_query = ' AND '.join(having)
                query += f" HAVING {having_query}"

            count_query = f"SELECT COUNT(*) AS count FROM ({query}) AS count"
            query = count_query

        try:
            cursor = conn.cursor()
            cursor.execute(query)

            result["total"] = int(cursor.fetchall()[0][0].decode("utf8"))

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def get_list_data(
            self,
            table: str,
            conditions: dict = None,
            custom_conditions: list = None,
            column_select: list = None,
            column_deselect: list = None,
            custom_columns: list = None,
            join: list = None,
            group_by: list = None,
            custom_orders: list = None,
            having: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None,
            "page": 1,
            "limit": 0
        }

        conn = self.__connect()

        if not conn.is_connected() or not table:
            return result

        columns = self.__check_column(table)
        master_columns = columns.copy()

        order = conditions["order"] if conditions and isinstance(conditions, dict) and isinstance(conditions.get("order"), str) else columns[0]

        if isinstance(order, str) and order in columns:
            order = order
        else:
            order = columns[0]

        sort_data = ['ASC', 'DESC']
        sort = sort_data[0]
        
        if conditions and isinstance(conditions, dict) and isinstance(conditions.get("sort"), str) and conditions["sort"].upper() in sort_data:
            sort = conditions["sort"].upper()

        limit = 20

        if conditions and isinstance(conditions, dict) and is_numeric(conditions.get("limit")):
            limit = conditions["limit"]

        page = conditions["page"] if conditions and isinstance(conditions, dict) and is_numeric(conditions.get("page")) and conditions["page"] > 0 else 1

        condition_query = []

        if column_select and isinstance(column_select, list):
            if not "*" in column_select:
                # filter data from all table columns, only keep selected columns
                columns = list(set(columns).intersection(column_select))

        if column_deselect and isinstance(column_deselect, list):
            if "*" in column_deselect:
                # filter data, exclude all columns
                columns = []
            else:
                # filter data, get column to exclude from valid selected columns or table columns
                column_deselect = set(columns).intersection(column_deselect)
                # filter data, exclude deselected columns
                columns = [col for col in columns if col not in column_deselect]

        if join and isinstance(join, list):
            # give prefix table to table columns
            columns = list(map(lambda col: f"{table}.{col}", columns))

        if custom_columns and isinstance(custom_columns, list):
            columns.extend(col for col in custom_columns if col not in columns)

        column = ", ".join(columns)
        query = f"SELECT {column} FROM {table}"

        if join and isinstance(join, list):
            join_query = " ".join(join)
            query += f" {join_query}"

        # remove invalid column from conditions
        conditions = filter_column_data(data=conditions, columns=master_columns)

        if conditions and isinstance(conditions, dict):
            for key in conditions:
                if isinstance(conditions[key], list):
                    condition_query.append(f"{table}.{key} IN ({', '.join(map(escape, conditions[key]))})")
                else:
                    condition_query.append(f"{table}.{key} = {escape(conditions[key])}")

        if custom_conditions and isinstance(custom_conditions, list):
            condition_query.extend(custom_conditions)

        if not is_empty(condition_query):
            condition_query = ' AND '.join(condition_query)
            query += f" WHERE {condition_query}"

        if group_by and isinstance(group_by, list):
            # strip each group column
            group_query = list(col.strip() for col in group_by)
            # add prefix table when group column in master columns
            group_query = list(f"{table}.{col}" if col in master_columns else col for col in group_query)
            # join group column
            group_query = ", ".join(group_query)

            query += f" GROUP BY {group_query}"

            if having and isinstance(having, list):
                having_query = ' AND '.join(having)
                query += f" HAVING {having_query}"

        if custom_orders and isinstance(custom_orders, list):
            order_query = ', '.join(custom_orders)
            query += f" ORDER BY {order_query} {sort}"
        else:
            if join and isinstance(join, list):
                order = f"{table}.{order}"

            query += f" ORDER BY {order} {sort}"

        if limit > 0:
            query += f" LIMIT {limit}"
            offset = (limit * page) - limit

            if offset >= 0:
                query += f" OFFSET {offset}"

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            fields = cursor.fetchall()

            if fields:
                result["total"] = self.count_data(
                    table=table,
                    conditions=conditions,
                    join=join,
                    group_by=group_by,
                    having=having
                )["total"]

                result["data"] = [dict((cursor.column_names[i], v.decode("utf8") if isinstance(v, (bytes, bytearray)) else v) for i, v in enumerate(row)) for row in fields]

                result["page"] = page

                result["limit"] = limit

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def get_row_data(
            self,
            table: str = None,
            conditions: dict = None,
            custom_conditions: list = None,
            column_select: list = None,
            column_deselect: list = None,
            custom_columns: list = None,
            join: list = None,
            group_by: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected():
            return result

        columns = []
        master_columns = []

        if table and isinstance(table, str):
            columns = self.__check_column(table)
            master_columns = columns.copy()

        order = None

        if conditions and isinstance(conditions, dict) and isinstance(conditions.get("order"), str) and conditions["order"] in columns:
            order = conditions["order"]

        sort_data = ['ASC', 'DESC']

        sort = sort_data[0] if order else None

        if conditions and isinstance(conditions, dict) and isinstance(conditions.get("sort"), str) and conditions["sort"].upper() in sort_data:
            sort = conditions["sort"].upper()

        limit = 1

        condition_query = []

        if column_select and isinstance(column_select, list):
            if not "*" in column_select:
                # filter data from all table columns, only keep selected columns
                columns = list(set(columns).intersection(column_select))

        if column_deselect and isinstance(column_deselect, list):
            if "*" in column_deselect:
                # filter data, exclude all columns
                columns = []
            else:
                # filter data, get column to exclude from valid selected columns or table columns
                column_deselect = set(columns).intersection(column_deselect)
                # filter data, exclude deselected columns
                columns = [col for col in columns if col not in column_deselect]

        if join and isinstance(join, list):
            # give prefix table to table columns
            columns = list(map(lambda col: f"{table}.{col}", columns))

        if custom_columns and isinstance(custom_columns, list):
            columns.extend(col for col in custom_columns if col not in columns)

        column = ", ".join(columns)
        query = f"SELECT {column}"

        if table and isinstance(table, str):
            query += f" FROM {table}"

        if join and isinstance(join, list):
            join_query = " ".join(join)
            query += f" {join_query}"

        # remove invalid column from conditions
        conditions = filter_column_data(data=conditions, columns=master_columns)

        if conditions and isinstance(conditions, dict):
            for key in conditions:
                if isinstance(conditions[key], list):
                    condition_query.append(f"{table}.{key} IN ({', '.join(map(escape, conditions[key]))})")
                else:
                    condition_query.append(f"{table}.{key} = {escape(conditions[key])}")

        if custom_conditions and isinstance(custom_conditions, list):
            condition_query.extend(custom_conditions)

        if not is_empty(condition_query):
            condition_query = ' AND '.join(condition_query)
            query += f" WHERE {condition_query}"

        if group_by and isinstance(group_by, list):
            # strip each group column
            group_query = list(col.strip() for col in group_by)

            if table and isinstance(table, str):
                # add prefix table when group column in master columns
                group_query = list(f"{table}.{col}" if col in master_columns else col for col in group_query)

            # join group column
            group_query = ", ".join(group_query)

            query += f" GROUP BY {group_query}"

        if order and isinstance(order, str):
            order_query = f"{table}.{order}" if join and isinstance(join, list) else order
            query += f" ORDER BY {order_query}"

            if sort and isinstance(sort, str):
                query += f" {sort}"

        query += f" LIMIT {limit}"

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            field = cursor.fetchone()

            if field:
                result["total"] = 1
                result["data"] = dict((cursor.column_names[i], v.decode("utf8") if isinstance(v, (bytes, bytearray)) else v) for i, v in enumerate(field))

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result
    
    def insert_data(
            self,
            table: str,
            data: dict,
            protected_columns: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected() or is_empty(table) or is_empty(data):
            return result

        time_char = ["CURRENT_TIMESTAMP()", "NOW()"]
        null_char = ["NONE", "None", "NULL", "Null", ""]

        columns = self.__check_column(table)

        # remove invalid column from data
        data = filter_column_data(data=data, columns=columns)

        if not data:
            return result

        keys = data.keys()

        # check protected columns on submitted data
        forbidden_columns = list(set(keys).intersection(protected_columns))

        if not is_empty(forbidden_columns):
            return result

        column = ", ".join(keys)
        placeholder = ", ".join(["%s"] * len(keys))
        query = f"INSERT INTO {table} ({column}) VALUES ({placeholder})"
        values = []

        for key in data:
            value = None

            if isinstance(data[key], datetime):
                value = data[key].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(data[key], date):
                value = data[key].strftime("%Y-%m-%d")
            elif isinstance(data[key], time):
                value = data[key].strftime("%H:%M:%S")
            elif isinstance(data[key], str):
                value = data[key].strip()

                if value in time_char:
                    value = data[key].replace(data[key], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif value in null_char:
                    value = None
                else:
                    value = data[key]
            else:
                if isinstance(data[key], str):
                    value = data[key].strip()

                    if value in time_char:
                        value = value.replace(value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    elif data[key] in null_char:
                        value = None
                elif data[key] is None:
                    value = None
                else:
                    value = data[key]

            values.append(value)

        # convert list to tuple
        values = tuple(values)

        try:
            cursor = conn.cursor()
            cursor.execute(query, values)

            affected_id = int(cursor.lastrowid)
            affected_rows = int(cursor.rowcount)

            result["total"] = affected_rows
            result["data"] = {"id": affected_id}

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def insert_many_data(
            self,
            table: str,
            data: list,
            protected_columns: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected() or is_empty(table) or is_empty(data):
            return result

        time_char = ["CURRENT_TIMESTAMP()", "NOW()"]
        null_char = ["NONE", "None", "NULL", "Null", ""]

        columns = self.__check_column(table)

        # remove invalid column from data
        data = filter_column_data(data=data, columns=columns)

        if is_empty(data):
            return result

        keys = data[0].keys()

        if is_empty(keys):
            return result

        # compare invalid data with columns
        difference_columns = list(set(keys) - set(columns))

        if not is_empty(difference_columns):
            return result

        # check protected columns on submitted data
        forbidden_columns = list(set(keys).intersection(protected_columns))

        if not is_empty(forbidden_columns):
            return result

        column = ", ".join(keys)
        placeholder = ", ".join(["%s"] * len(keys))
        query = f"INSERT INTO {table} ({column}) VALUES ({placeholder})"
        values = []

        for i, _ in enumerate(data):
            if not isinstance(data[i], dict) and keys != data[i].keys():
                return result

            temp_values = []

            for key in data[i]:
                value = None

                if isinstance(data[i][key], datetime):
                    value = data[i][key].strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(data[i][key], date):
                    value = data[i][key].strftime("%Y-%m-%d")
                elif isinstance(data[i][key], time):
                    value = data[i][key].strftime("%H:%M:%S")
                elif isinstance(data[i][key], str):
                    value = data[i][key].strip()

                    if value in time_char:
                        value = data[i][key].replace(data[i][key], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    elif value in null_char:
                        value = None
                    else:
                        value = data[i][key]
                else:
                    if isinstance(data[i][key], str):
                        value = data[i][key].strip()

                        if value in time_char:
                            value = value.replace(value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        elif data[i][key] in null_char:
                            value = None
                    elif data[i][key] is None:
                        value = None
                    else:
                        value = data[i][key]

                temp_values.append(value)

            values.append(tuple(temp_values))

        try:
            cursor = conn.cursor()
            cursor.executemany(query, values)

            affected_id = int(cursor.lastrowid)
            affected_rows = int(cursor.rowcount)

            result["total"] = affected_rows
            result["data"] = list({"id": x} for x in range(affected_id, affected_id + affected_rows))

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def insert_many_update_data(
            self,
            table: str,
            data: list,
            protected_columns: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected() or is_empty(table) or is_empty(data):
            return result

        time_char = ["CURRENT_TIMESTAMP()", "NOW()"]
        null_char = ["NONE", "None", "NULL", "Null", ""]

        columns = self.__check_column(table)

        # remove invalid column from data
        data = filter_column_data(data=data, columns=columns)

        if is_empty(data):
            return result

        keys = data[0].keys()
        
        if is_empty(keys):
            return result

        # compare invalid data with columns
        difference_columns = list(set(keys) - set(columns))

        if not is_empty(difference_columns):
            return result

        # check protected columns on submitted data
        forbidden_columns = list(set(keys).intersection(protected_columns))

        if not is_empty(forbidden_columns):
            return result

        column = ", ".join(keys)
        placeholder = ", ".join(["%s"] * len(keys))
        update_values = ", ".join([f"{v} = VALUES({v})" for v in keys])
        query = f"INSERT INTO {table} ({column}) VALUES ({placeholder}) ON DUPLICATE KEY UPDATE {update_values}"
        values = []

        for i, _ in enumerate(data):
            # if index and 'data' on each object not the same
            if not isinstance(data[i], dict) and keys != data[i].keys():
                return result

            temp_values = []

            for key in data[i]:
                value = None

                if isinstance(data[i][key], datetime):
                    value = data[i][key].strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(data[i][key], date):
                    value = data[i][key].strftime("%Y-%m-%d")
                elif isinstance(data[i][key], time):
                    value = data[i][key].strftime("%H:%M:%S")
                elif isinstance(data[i][key], str):
                    value = data[i][key].strip()

                    if value in time_char:
                        value = data[i][key].replace(data[i][key], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    elif value in null_char:
                        value = None
                    else:
                        value = data[i][key]
                else:
                    if isinstance(data[i][key], str):
                        value = data[i][key].strip()

                        if value in time_char:
                            value = value.replace(value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        elif data[i][key] in null_char:
                            value = None
                    elif data[i][key] is None:
                        value = None
                    else:
                        value = data[i][key]

                temp_values.append(value)

            values.append(tuple(temp_values))

        try:
            cursor = conn.cursor()
            cursor.executemany(query, values)

            affected_id = int(cursor.lastrowid)
            affected_rows = int(cursor.rowcount)

            result["total"] = affected_rows
            result["data"] = data

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def update_data(
            self,
            table: str,
            data: dict,
            conditions: dict,
            protected_columns: list = None
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected() or is_empty(table) or is_empty(data) or is_empty(conditions):
            return result

        time_char = ["CURRENT_TIMESTAMP()", "NOW()"]
        null_char = ["NONE", "None", "NULL", "Null", ""]

        columns = self.__check_column(table)

        # remove invalid column from data
        data = filter_column_data(data=data, columns=columns)

        if not data:
            return result

        keys = data.keys()

        # check protected columns on submitted data
        forbidden_columns = list(set(keys).intersection(protected_columns))

        if not is_empty(forbidden_columns):
            return result

        condition_query = []
        set_query = []
        query = f"UPDATE {table}"
 
        for key in data:
            value = None

            if isinstance(data[key], datetime):
                value = data[key].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(data[key], date):
                value = data[key].strftime("%Y-%m-%d")
            elif isinstance(data[key], time):
                value = data[key].strftime("%H:%M:%S")
            elif isinstance(data[key], str):
                value = data[key].strip()

                if value in time_char:
                    value = data[key].replace(data[key], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif value in null_char:
                    value = None
                else:
                    value = data[key]
            else:
                if isinstance(data[key], str):
                    value = data[key].strip()

                    if value in time_char:
                        value = value.replace(value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    elif data[key] in null_char:
                        value = None
                elif data[key] is None:
                    value = None
                else:
                    value = data[key]

            if value is None:
                set_query.append(f"{key} = NULL")
            else:
                set_query.append(f"{key} = {escape(value)}")

        set_query = ", ".join(set_query)
        query += f" SET {set_query}"

        for key in conditions:
            if isinstance(conditions[key], list):
                condition_query.append(f"{table}.{key} IN ({', '.join(map(escape, conditions[key]))})")
            else:
                condition_query.append(f"{table}.{key} = {escape(conditions[key])}")

        condition_query = " AND ".join(condition_query)
        query += f" WHERE {condition_query}"

        try:
            cursor = conn.cursor()
            cursor.execute(query)

            affected_rows = int(cursor.rowcount)

            result["total"] = 1
            result["data"] = conditions

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result

    def delete_data(
            self,
            table: str,
            conditions: dict
        ) -> dict :
        result = {
            "total": 0,
            "data": None
        }

        conn = self.__connect()

        if not conn.is_connected() or is_empty(table) or is_empty(conditions):
            return result

        condition_query = []
        query = f"DELETE FROM {table}"
 
        for key in conditions:
            if isinstance(conditions[key], list):
                condition_query.append(f"{table}.{key} IN ({', '.join(map(escape, conditions[key]))})")
            else:
                condition_query.append(f"{table}.{key} = {escape(conditions[key])}")

        condition_query = " AND ".join(condition_query)
        query += f" WHERE {condition_query}"

        try:
            cursor = conn.cursor()
            cursor.execute(query)

            affected_rows = int(cursor.rowcount)

            result["total"] = affected_rows
            result["data"] = conditions

            conn.close()
        except Exception as err:
            result["error"] = str(err)

        return result