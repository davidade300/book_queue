from sqlalchemy import (
    Insert,
    Update,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session

from book_queue.models.models import Chapter, Note
from book_queue.core.schemas import CreateNoteRequest, UpdateNoteRequest


class NoteService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateNoteRequest) -> Note:
        """
        Create a new note from a CreateNoteRequest BaseModel.
        :param data: object of CreateNoteRequest type
        :return: note:Note
        """

        stmt: Insert = (
            insert(Note)
            .values(
                **data.model_dump(),
            )
            .returning(Note)
        )

        note: Note = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return note

    def get_by_id(self, note_id: int) -> Note:
        """
        return a note by it's id
        :param note_id: int representin the id of the searched note
        :return: note:Note
        """
        stmt = select(Note).where(Note.id == note_id)
        note = self.db.execute(stmt).scalar_one()

        return note

    def update(self, note_id: int, data: UpdateNoteRequest) -> Note:
        """
        update a note by it's id, dumping a updateNoteRequest object data in the note
        of said id
        :param note_id: int representing the id of the note to update
        :param data: UpdateNoteRequest object data
        :return: note:Note
        """
        update_data: dict[str, str] = data.model_dump(
            exclude_none=True, exclude_unset=True
        )

        if data.title:
            update_data['title'] = data.title.title().strip()

        stmt: Update = (
            update(Note).where(Note.id == note_id).values(**update_data)
        ).returning(Note)

        note: Note = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return note

    def delete(self, note_id: int) -> None:
        """
        Delete a note by it's id
        :param note_id:
        :return: boolean or raises get_by_id function exception
        """
        note = self.get_by_id(note_id)

        self.db.delete(note)
        self.db.commit()

    def list_by_chapter_id(self, chapter_id: int) -> list[Note]:
        """
        list a chapter's notes
        :param chapter_id: id of the chapter to list it's notes
        :return: list of notes
        """
        stmt = select(Note).where(Note.chapter_id == chapter_id)
        notes: list[Note] = list[Note](self.db.execute(stmt).scalars().all())

        return notes

    def list_by_book_id(self, book_id: int) -> list[Note]:
        """
        list a book notes by the book id
        :param book_id: id of the book to list it's notes
        :return: a list of notes
        """
        stmt = (
            select(Note)
            .join(Chapter)
            .where(Chapter.book_id == book_id)
            .order_by(Note.created_at.desc())
        )

        notes: list[Note] = list[Note](self.db.execute(stmt).scalars().all())

        return notes
