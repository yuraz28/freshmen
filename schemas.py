from uuid import UUID
from pydantic import BaseModel
import orjson
from typing import Optional, List


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UserAllInfo(BaseSchema):
    name: str
    email: str
    place_study: str
    password_hash: str
    branch: str
    course: int
    is_user: bool


class UserAuth(BaseSchema):
    email: str
    password_hash: str


class UserGet(BaseSchema):
    id: str
    email: str
    password_hash: str


class CheckEmail(BaseSchema):
    email: str


class CheckAnswer(BaseSchema):
    answer: bool


class AddFile(BaseSchema):
    name: str
    place_study: str
    author_id: UUID
    branch: str
    course: int
    is_private: bool


class AddReview(BaseSchema):
    text: str
    author_id: Optional[str]
    branch: Optional[str]


class InfoFile(BaseSchema):
    id: UUID
    name: str
    place_study: str
    author_id: UUID
    branch: str
    course: int
    is_private: bool


class DownloadFile(BaseModel):
    place_study: List[InfoFile]
    branch: List[InfoFile]
    place_study_branch: List[InfoFile]
    place_study_branch_course: List[InfoFile]
