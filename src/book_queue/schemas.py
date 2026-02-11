from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateNoteRequest(BaseModel):
    title: str
    content: str
    chapter_id: int


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    chapter_id: int
    created_at: datetime
    last_updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateNoteRequest(BaseModel):
    title: str | None = None
    content: str | None = None


class CreateChapterRequest(BaseModel):
    title: str
    summary: str
    book_id: int


class ChapterResponse(BaseModel):
    id: int
    title: str
    summary: str
    book_id: int
    notes: list[NoteResponse] | None = None
    created_at: datetime
    last_updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateChapterRequest(BaseModel):
    summary: str
