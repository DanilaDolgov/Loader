from aiohttp.web import Response

from drive_server.app.base.application import View


class FileDownloadView(View):
    async def post(self):
        from_button = await self.request.json()
        result = await self.store.s3.get_object(key=from_button['key'])
        return Response(body=bytearray(result), headers={'Content-Type': 'application/octet-stream'})
