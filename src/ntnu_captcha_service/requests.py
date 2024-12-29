import io

from fastapi import HTTPException, Request
from PIL import Image


async def image_request(request: Request):
    data: bytes = await request.body()
    image = Image.open(io.BytesIO(data))
    if image.get_format_mimetype() != request.headers["Content-Type"]:
        raise HTTPException(
            status_code=415,
            detail={
                "msg": "MIME type and content mismatch",
                "given": request.headers["Content-Type"],
                "identified": image.get_format_mimetype(),
            },
        )
    return image
