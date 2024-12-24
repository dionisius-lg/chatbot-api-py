import os
import json
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from app.helpers.response import not_found as send_not_found
from app.helpers.encryption import decrypt

__route = os.path.splitext(os.path.basename(__file__))[0]
router = APIRouter(prefix=f"/{__route}", tags=[__route])

@router.get("/{id}")
async def download(id: str, response: Response):
    try:
        decrypted = decrypt(id)

        if decrypted is None:
            raise ValueError("File not found")

        data = json.loads(decrypted)

        mimetype = data.get("mimetype", "")
        filename = data.get("filename", "")
        path = data.get("path", "/")
        size = data.get("size", 0)
        destination = f"{path}/{filename}"

        if not os.path.exists(destination):
            raise ValueError("File not found")

        # set appropriate headers for file download
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = mimetype
        response.headers["Content-Length"] = str(size)

        return FileResponse(destination)
    except Exception as e:
        return send_not_found(str(e))