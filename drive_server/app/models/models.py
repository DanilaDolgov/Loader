from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,

)
from sqlalchemy.orm import relationship
from drive_server.app.database.database_sqlalchemy import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


class DownlodedFiles(Base):
    __tablename__ = "files_user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, lazy="joined")
    file_name = Column(String(200), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
