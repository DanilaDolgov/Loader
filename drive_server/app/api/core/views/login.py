import bcrypt
from pydantic.error_wrappers import ValidationError

from drive_server.app.api.utils.users import check_hash_pass
from drive_server.app.base.application import View
from drive_server.app.web.response import json_response
from aiohttp.web_response import json_response
import aiohttp_session
from aiohttp import web
from drive_server.app.models.models import User
from drive_server.app.schemas.users import User as UserValidPydantic


class CoreLoginView(View):
    async def post(self):
        user_client = UserValidPydantic(**self.request["json_data"])
        user_db = await self.app.store.postgres_user.get_user(user_client.username)
        if user_db is None:
            raise web.HTTPForbidden(reason='Пользователь не зарегистрирован!')
        if user_client.username != user_db.username or check_hash_pass(user_client, user_db) == False:
            raise web.HTTPForbidden(reason='Неверная пара логин/пароль!')
        session = await aiohttp_session.new_session(request=self.request)
        session['user'] = {
            'id': user_db.id
        }
        self.app.logger.info(f'success login for user - {user_client.username}')
        return json_response(data={})


class AddUserView(View):
    async def post(self):
        try:
            user_client = UserValidPydantic(**self.request["json_data"])
        except ValidationError:
            raise web.HTTPForbidden(reason='not valid email')
        user_db = await self.app.store.postgres_user.get_user(user_client.username)
        if user_db is None:
            new_user = User(username=user_client.username,
                            password=bcrypt.hashpw(user_client.password.encode('utf-8'), bcrypt.gensalt()).decode())
            await self.request.app.store.postgres_user.add_user(new_user)
            return json_response(data={'status': 'ok', 'data_reg': f'{new_user.username, new_user.password,}'})
        else:
            self.app.logger.info('user already exist')
            return json_response(data={'status': 'ok', 'data_reg': 'user already exist'})
