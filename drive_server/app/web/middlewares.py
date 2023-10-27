from aiohttp.web_middlewares import middleware
from aiohttp_session import get_session

from drive_server.app.base.application import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    user_id = session.get("user").get("id") if session.get("user", None) is not None else None
    request.user_id = user_id
    return await handler(request)


@middleware
async def request_json(request: "Request", handler: callable):
    if request.user_id is None:
        json_data = await request.text() if await request.text() is not '' else None
        if json_data is not None:
            request["json_data"] = await request.json()
            return await handler(request)
    return await handler(request)


def setup_middlewares(app: Application):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(request_json)
