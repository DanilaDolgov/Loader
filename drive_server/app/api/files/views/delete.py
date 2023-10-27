from drive_server.app.base.application import View
from drive_server.app.web.response import json_response


class FilesDeleteView(View):
    async def post(self):
        from_button = await self.request.json()
        await self.store.s3.delete_object(key=from_button['key'])
        return json_response()
