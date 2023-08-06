from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

# Users


class CreateUserRestModel(BaseModel):
    name: str
    email: str
    temporal: bool


class UserRestModel(BaseModel):
    id: str
    name: str
    email: str
    temporal: bool
    created: str
    last_modified: str


class UserSearchCriteriaRestModel(BaseModel):
    name: Optional[str]
    email: Optional[str]


# Tasks

class TaskRestModel(BaseModel):
    id: str
    name: str
    created: str
    last_modified: str
    extensions: List[str]
    submission_ids: List[str]
    check_ids: List[str]


class CreateTaskRequestRestModel(BaseModel):
    user_id: str
    name: str
    extensions: List[str]


class CreateTaskResponseRestModel(BaseModel):
    id: str


class MutipleTasksRestModel(BaseModel):
    id: str
    name: str
    created: str
    last_modified: str
    extensions: List[str]
    submissions_total: int
    checks_total: int


class UpdateTaskRestModel(BaseModel):
    name: Optional[str]
    extensions: Optional[List[str]]
    submission_ids: Optional[List[str]]
    check_ids: Optional[List[str]]


class MulptipleTasksRestModel(BaseModel):
    total: int
    tasks: List[MutipleTasksRestModel]


# Files

class CreateFileRestModel(BaseModel):
    user_id: str
    path: str
    name: str
    extension: str
    content_type: str
    content: str


class MutipleFilesRestModel(BaseModel):
    id: str
    path: str
    name: str
    extension: str
    content_type: str

# Submissions


class CreateSubmissionRestModel(BaseModel):
    user_id: str
    name: str
    file_ids: List[str]


class FileInfoRestModel(BaseModel):
    path: str
    name: str
    extension: str


class MultipleSubmissionRestModel(BaseModel):
    id: str
    name: str
    created: str
    last_modified: str
    files_info: List[FileInfoRestModel]


class SubmissionRestModel(BaseModel):
    id: str
    name: str
    task_id: str
    created: str
    last_modified: str
    file_ids: List[str]


# Checks


class FileResultRestModel(BaseModel):
    id: str
    submission_id: Optional[str]
    path: str
    name: str
    extension: str
    match_percentage: float
    total_lines_matched: int
    lines_matched: List[Tuple[str, int, int]]


class CheckMatchRestModel(BaseModel):
    id: str
    source_file: FileResultRestModel
    target_file: FileResultRestModel


class CreateCheckRestModel(BaseModel):
    user_id: str
    name: str
    status: str
    task_id: Optional[str]
    matches: List[CheckMatchRestModel]


class SingleCheckRestModel(BaseModel):
    id: str
    name: str
    task_id: Optional[str]
    status: str
    created: str
    last_modified: str


class SingleMulptipleCheckRestModel(BaseModel):
    id: str
    name: str
    task_id: Optional[str]
    status: str
    created: str
    last_modified: str


class MulptipleChecksRestModel(BaseModel):
    total: int
    checks: List[SingleMulptipleCheckRestModel]


class UpdateCheckRestModel(BaseModel):
    status: str
    matches: List[CheckMatchRestModel]
    metrics: Dict[str, Any]


class SingleCheckMatchesRestModel(BaseModel):
    total: int
    matches: List[CheckMatchRestModel]
