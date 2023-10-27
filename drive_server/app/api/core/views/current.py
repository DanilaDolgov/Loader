from aiohttp import web
from aiohttp.web_response import json_response
from drive_server.app.base.application import View


class CoreCurrentView(View):
    async def get(self):
        if not self.request.user_id:
            raise web.HTTPUnauthorized
        return json_response(data={})
