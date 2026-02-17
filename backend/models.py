from pydantic import BaseModel


class UploadResponse(BaseModel):
    session_id: str
    page_count: int
    original_filename: str


class SplitRequest(BaseModel):
    session_id: str
    original_filename: str
    pages: list[int]
