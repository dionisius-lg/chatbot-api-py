from app.helpers.value import is_empty

def filter_data(data: list|dict) -> list|dict :
    if isinstance(data, list):
        for i, _ in enumerate(data.copy()):
            if isinstance(data[i], dict):
                for key in data[i].copy():
                    if key and not is_empty(data[i][key]):
                        val = data[i][key].strip() if isinstance(data[i][key], str) else data[i][key]

                        data[i][key] = val
                    else:
                        del data[i][key]
            else:
                del data[i][key]

    if isinstance(data, dict):
        for key in data.copy():
            if key and not is_empty(data[key]):
                val = data[key].strip() if isinstance(data[key], str) else data[key]

                data[key] = val
            else:
                del data[key]

    return data

def filter_column_data(data: list|dict, columns: list|dict) -> list|dict:
    if isinstance(data, list):
        for i, _ in enumerate(data.copy()):
            if isinstance(data[i], dict):
                for key in data[i].copy():
                    if key and not is_empty(data[i][key]):
                        val = data[i][key].strip() if isinstance(data[i][key], str) else data[i][key]

                        if key not in columns:
                            del data[i][key]
                            continue

                        if isinstance(columns, dict) and data[i][key] is None and columns[key]["type"] in ["int", "tinyint", "mediumint", "bigint"]:
                            val = 0

                        data[i][key] = val
                    else:
                        del data[i][key]
            else:
                del data[i][key]

    if isinstance(data, dict):
        for key in data.copy():
            if key and not is_empty(data[key]):
                val = data[key].strip() if isinstance(data[key], str) else data[key]

                if key not in columns:
                    del data[key]
                    continue

                if isinstance(columns, dict) and data[i][key] is None and columns[key]["type"] in ["int", "tinyint", "mediumint", "bigint"]:
                    val = 0

                data[key] = val
            else:
                del data[key]

    return data