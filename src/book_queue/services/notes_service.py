from sqlalchemy import (
    Insert,
    Select,
    Update,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session

from book_queue.models.models import Note
from book_queue.schemas import CreateNoteRequest, UpdateNoteRequest


class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateNoteRequest) -> Note:
        try:
            stmt: Insert = (
                insert(Note)
                .values(
                    title=data.title.title().strip(),
                    content=data.content,
                    chapter_id=data.chapter_id,
                )
                .returning(Note)
            )

            note: Note = self.db.execute(stmt).scalar_one()
            self.db.commit()

            return note
        except Exception:
            raise Exception('Ops something went wrong')

    def update(self, note_id: int, data: UpdateNoteRequest) -> Note:
        try:
            update_data: dict[str, str] = data.model_dump(
                exclude_none=True, exclude_unset=True
            )

            if data.title:
                update_data['title'] = data.title.title().strip()

            stmt: Update = (
                update(Note).where(Note.id == note_id).values(**update_data)
            )

            note: Note = self.db.execute(stmt).scalar_one()
            self.db.commit()

            return note
        except Exception:
            raise Exception(f'Note with id {note_id} not found')

    def delete(self, note_id: int) -> bool:
        stmt = select(Note).where(Note.id == note_id)
        note = self.db.execute(stmt).scalar()

        if not note:
            raise Exception(f'Note with id {note_id} not found')

        self.db.delete(note)
        self.db.commit()

        return True

    def list_by_chapter_id(self, chapter_id: int) -> list[Note]:
        stmt = select(Note).where(Note.chapter_id == chapter_id)
        notes: list[Note] = list[Note](self.db.execute(stmt).scalars().all())

        return notes

    def list_by_book_id(self, book_id: int) -> list[Note]:
        ...
        # TODO: implement method
