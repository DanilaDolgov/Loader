import bcrypt
from drive_server.app.schemas.users import User as UserValidPydantic


def check_hash_pass(client_pass: UserValidPydantic, db_pass):
    return bcrypt.checkpw(client_pass.password.encode('utf-8'),
                          db_pass.password.encode('utf-8'))
