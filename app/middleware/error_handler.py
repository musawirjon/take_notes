from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def error_handler_middleware(
    request: Request,
    call_next
) -> Union[Response, JSONResponse]:
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "path": request.url.path
            }
        ) 