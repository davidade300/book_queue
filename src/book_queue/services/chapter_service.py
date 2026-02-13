from sqlalchemy import Update, insert, select, update
from sqlalchemy.orm import Session

from book_queue.models.models import Chapter, Note
from book_queue.core.schemas import CreateChapterRequest


class ChapterService:
    def __init__(self, db: Session):
        self.db: Session = db

    def create(self, data: CreateChapterRequest) -> Chapter:
        stmt = insert(Chapter).values(**data.model_dump()).returning(Chapter)

        chapter: Chapter = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return chapter

    def get_by_id(self, chapter_id: int) -> Chapter:
        stmt = select(Chapter).where(Chapter.id == chapter_id)
        chapter: Chapter = self.db.execute(stmt).scalar_one()

        return chapter


    def list_chapters(self) -> list[Chapter]:
        stmt = select(Chapter).order_by(Chapter.created_at.desc())
        chapters: list[Chapter] = list[Chapter](
            self.db.execute(stmt).scalars().all()
        )

        return chapters

    def update(self, chapter_id: int, data: CreateChapterRequest) -> Chapter:
        stmt: Update = (
            update(Chapter)
            .where(Chapter.id == chapter_id)
            .values(**data.model_dump())
            .returning(Chapter)
        )

        updated_chapter = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return updated_chapter

    def delete(self, chapter_id: int) -> None:
        chapter: Chapter = self.get_by_id(chapter_id)

        self.db.delete(chapter)
        self.db.commit()

    def list_by_book_id(self, book_id: int) -> list[Chapter]:
        stmt = select(Chapter).where(Chapter.book_id == book_id)
        chapters: list[Chapter] = list[Chapter](
            self.db.execute(stmt).scalars().all()
        )

        return chapters

    def get_by_note_id(self, note_id: int) -> Chapter:
        stmt = select(Chapter).join(Note).where(Note.id == note_id)
        chapter: Chapter = self.db.execute(stmt).scalar_one()

        return chapter
