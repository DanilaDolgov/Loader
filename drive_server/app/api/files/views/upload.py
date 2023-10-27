import uuid
from aiohttp.web import json_response
from drive_server.app.api.files.utils import make_upload_callback
from drive_server.app.base.application import View
from drive_server.app.store.websockets.websocket_accessor import WebSocketMessageKind
from drive_server.app.models.models import DownlodedFiles


class FilesUploadView(View):
    async def post(self):
        raw_upload_id = self.request.headers.get('X-Upload-Id')
        upload_id = uuid.UUID(raw_upload_id)
        from_fields = await self.request.multipart()
        reader, filename = None, None
        async for field in from_fields:
            if field.name == "file":
                reader = field
                filename = field.filename
                break
        content_length = self.request.headers.get('Content-Length')
        total_size = int(content_length)

        new_file = DownlodedFiles(user_id=int(self.request.user_id), file_name=filename)
        if await self.store.postgres_user.get_file(user_id=new_file.user_id, filename=new_file.file_name) is None:
            await self.request.app.store.postgres_user.downloads(new_file)

        callback = make_upload_callback(self.store, self.request.user_id, upload_id, total_size)
        await self.store.s3.upload(key=filename, reader=reader, upload_callback=callback)
        await self.store.ws.push(self.request.user_id, kind=WebSocketMessageKind.UPLOAD_FINISH,
                                 data={
                                     'upload_id': str(upload_id)
                                 })
        return json_response()
