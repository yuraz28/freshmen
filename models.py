import ormar
from core.db import BaseMeta
from uuid import UUID, uuid4
from passlib.hash import bcrypt
import datetime


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    name: str = ormar.String(max_length=100, nullable=False)
    email: str = ormar.String(max_length=100, nullable=False, unique=True)
    place_study: str = ormar.String(max_length=100, nullable=False)
    password_hash: str = ormar.String(max_length=128)
    branch: str = ormar.String(max_length=10, nullable=False)
    course: int = ormar.SmallInteger(nullable=False)
    is_user: bool = ormar.Boolean(nullable=False)

    @classmethod
    async def get_user(cls, email):
        return cls.get(email=email)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Review(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    text: str = ormar.Text(nullable=False)
    branch: str = ormar.String(max_length=10, nullable=False)
    author_id: UUID = ormar.UUID(nullable=False)


class Paths_file(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    name: str = ormar.String(max_length=100, nullable=False)
    author_id: UUID = ormar.UUID(nullable=False)
    place_study: str = ormar.String(max_length=100, nullable=False)
    branch: str = ormar.String(max_length=10, nullable=False)
    course: int = ormar.SmallInteger(nullable=False)
    is_private: bool = ormar.Boolean(nullable=False)
