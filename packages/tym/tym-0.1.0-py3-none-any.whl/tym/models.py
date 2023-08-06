from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class RequestError(Exception):
    def __init__(self, data: Optional[dict] = None):
        self.data = data

    def __str__(self) -> str:
        error_message = type(self).__name__
        if self.data != None:
            error_message += f" - {self.data}"
        return error_message


class AuthenticationError(RequestError):
    pass


class RepoError(RequestError):
    pass


class ServerError(Exception):
    pass


class VersionError(Exception):
    pass


class RepoState:
    Merged = "merged"
    Active = "active"
    Archived = "archived"
    Deleted = "deleted"
    Error = "error"


class TymRepo(BaseModel):
    id: str
    state: str
    tym_remotes: List[str]


class Commit(BaseModel):
    id: str
    message: str
    author: str
    timestamp: int
    parent_ids: List[str]


class ShadowCommit(Commit):
    shadow_parent_id: Optional[str]
    official_parent_id: Optional[str]
