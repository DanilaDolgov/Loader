from drive_server.app.base.application import View
from drive_server.app.web.response import json_response

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class FilesListView(View):
    async def get(self):
        user_id = self.request.user_id
        files = await self.store.s3.list_objects(user_id)
        return json_response({'items': files[::-1]})
