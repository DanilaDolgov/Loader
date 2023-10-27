import os
from aiohttp import web

from drive_server.app.base.application import View
from main import BASE_DIR
from drive_server.app.settings import settings


class IndexView(View):
    async def get(self):
        with open(os.path.join(BASE_DIR, 'drive_server', 'app', 'templates', 'index.html'), 'r') as f:
            file = f.read()

        file = file.replace('{{API_HOST}}', os.environ.get('API_EXPOSER_URL', settings.BASE_URL))
        return web.Response(body=file, headers={
            'Content-Type': 'text/html',
        })
