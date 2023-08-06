from typing import List, Optional, Tuple

from pydantic import BaseModel

# Users models #


class UserRestModel(BaseModel):
    id: str
    name: str
    email: str
    temporal: bool
    created: str
    last_modified: str


class SignInRestModel(BaseModel):
    token_id: str


class LoginResponseModel(BaseModel):
    access_token: str


# Files models #


class CreateFileRestModel(BaseModel):
    path: str
    name: str
    extension: str
    content_type: str
    content: str

# Submissions models #


class CreateSubmissionRequestRestModel(BaseModel):
    name: str
    file_ids: List[str]


class CreateSubmissionStorageRequestRestModel(BaseModel):
    user_id: str
    name: str
    file_ids: List[str]


class SubmissionRestModel(BaseModel):
    id: str
    name: str
    file_ids: List[str]


# Tasks models #


class TaskRestModel(BaseModel):
    id: str
    name: str
    submission_ids: List[str]
    check_ids: List[str]


class CreateTaskRequestRestModel(BaseModel):
    name: str
    extensions: List[str]


class CreateTaskStorageRequestRestModel(BaseModel):
    user_id: str
    name: str
    extensions: List[str]


class UpdateTaskRestModel(BaseModel):
    name: Optional[str]
    submission_ids: Optional[List[str]]
    check_ids: Optional[List[str]]

# Checks models #


class OptionsRestModel(BaseModel):
    ignore_files: List[str]


class CreateCheckRestModel(BaseModel):
    check_name: str
    algorithm_name: str
    task_id: Optional[str]
    file_groups_ids: Optional[List[List[str]]]
    options: Optional[OptionsRestModel]


class CreateCheckRunnerRestModel(BaseModel):
    id: str
    check_name: str
    algorithm_name: str
    file_groups_ids: List[List[str]]
    options: Optional[OptionsRestModel]


class FileResultRestModel(BaseModel):
    id: str
    submission_id: Optional[str]
    name: str
    match_percentage: float
    total_lines_matched: int
    lines_matched: List[Tuple[str, int, int]]


class CheckMatchRestModel(BaseModel):
    id: str
    source_file: FileResultRestModel
    target_file: FileResultRestModel


class CreateCheckStorageRestModel(BaseModel):
    user_id: str
    name: str
    status: str
    task_id: Optional[str]
    matches: List[CheckMatchRestModel]


class CreateCheckResponseStorageRestModel(BaseModel):
    id: str
