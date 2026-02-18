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
    last_updated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateNoteRequest(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponseList(BaseModel):
    notes: list[NoteResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )


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
    last_updated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class ChapterResponseList(BaseModel):
    chapters: list[ChapterResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateChapterRequest(BaseModel):
    summary: str


class CreateBookRequest(BaseModel):
    title: str
    author: str
    edition: int
    release_date: datetime
    publisher: str
    cover_img_url: str
    isbn_10: str | None  # in clase the book is old or self published
    isbn_13: str | None  # in clase the book is old or self published


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    edition: int
    release_date: datetime
    publisher: str
    isbn_10: str | None = None
    isbn_13: str | None = None
    cover_img_url: str
    chapters: list[ChapterResponse] | None = None
    created_at: datetime
    last_updated_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class BookResponseList(BaseModel):
    books: list[BookResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )
