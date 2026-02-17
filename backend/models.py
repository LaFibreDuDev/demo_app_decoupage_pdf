from pydantic import BaseModel


class UploadResponse(BaseModel):
    session_id: str
    page_count: int
