from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


class OptionsRestModel(BaseModel):
    ignore_files: List[str]


class CreateCheckRestModel(BaseModel):
    id: str
    check_name: str
    algorithm_name: str
    file_groups_ids: List[List[str]]
    options: Optional[OptionsRestModel]


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


class UpdateCheckRestModel(BaseModel):
    status: str
    matches: List[CheckMatchRestModel]
    metrics: Dict[str, Any]
