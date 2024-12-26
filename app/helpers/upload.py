import os
import shutil
from fastapi import File, UploadFile, Depends
from datetime import datetime
from app.helpers.response import bad_request as send_bad_request
from app.helpers.value import is_empty
from app.config import file_dir

async def single_file(file: File, sub_path: str = "", size_limit: int = 1, mime_types: list[str] = None):
    result = {
        "mimetype": file.content_type,
        "destination": "",
        "filename": file.filename,
        "path": "",
        "size": 0,
        "error": None
    }

    # read the file contents to check size
    file_content = await file.read()
    result["size"] = len(file_content)

    # check file size
    if result["size"] > size_limit * 1024 * 1024: # size limit in MB
        result["error"] = f"File size exceeds {size_limit} MB"
        return result
        
    # validate file mimetype
    if isinstance(mime_types, list) and not is_empty(mime_types):
        if result["mimetype"] not in mime_types:
            mime_types_str = ", ".join(mime_types)
            result["error"] = f"Invalid file type. Allowed types: {mime_types_str}"
            return result

    ymd = datetime.now().strftime("%Y/%m/%d")
    result["path"] = f"{file_dir}/{ymd}"

    if isinstance(sub_path, str) and not is_empty(sub_path):
        sub_path = sub_path.replace('//', '/').strip('/')
        result["path"] = f"{file_dir}/{sub_path}/{ymd}"

    # create the directory if not exist
    os.makedirs(result["path"], exist_ok=True)

    result["destination"] = "%s/%s" % (result["path"], result["filename"])

    # save the file to the destination
    with open(result["destination"], "wb") as f:
        f.write(file_content)

    return result