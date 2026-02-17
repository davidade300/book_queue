from sqlalchemy import Update, insert, select, update
from sqlalchemy.orm import Session

from book_queue.core.schemas import CreateChapterRequest, UpdateChapterRequest
from book_queue.models.models import Chapter, Note


class ChapterService:
    """
    This class is a base service for the Chapter model
    """

    def __init__(self, db: Session):
        self.db: Session = db

    def create(self, data: CreateChapterRequest) -> Chapter:
        """
        Create a new chapter from a CreateChapterRequest BaseModel.
        :param data: object o CreateChapterRequest type
        :return: chapter:Chapter
        """
        stmt = insert(Chapter).values(**data.model_dump()).returning(Chapter)

        chapter: Chapter = self.db.execute(stmt).scalar_one()
        self.db.commit()

        return chapter

    def get_by_id(self, chapter_id: int) -> Chapter:
        """
        return a chapter by it's id
        :param chapter_id: int representing the chapter id
        :return: chapter:Chapter
        """
        stmt = select(Chapter).where(Chapter.id == chapter_id)
        chapter: Chapter = self.db.execute(stmt).scalar_one()

        return chapter

    def list_chapters(self) -> list[Chapter]:
        """
        return a list of all chapters of all books
        :return: list of chapters
        """
        stmt = select(Chapter).order_by(Chapter.created_at.desc())
        chapters: list[Chapter] = list[Chapter](
            self.db.execute(stmt).scalars().all()
        )

        return chapters

    def update(self, chapter_id: int, data: UpdateChapterRequest) -> Chapter:
        """
        Update a chapter by it's id, dumping a UpdateChapterRequest object data
        in the chapter of said id
        :param chapter_id: int representing the id of the chapter to update
        :param data: UpdateChapterRequest object data
        :return: chapter:Chapter
        """
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
        """
        delete a chapter by it's id
        :param chapter_id: int representing the id of the chapter to delete
        :return: None
        """
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
        """
        retrieve a chapter by it's id
        :param note_id: int representing the id of the chapter to retrieve
        :return: chapter:Chapter
        """
        stmt = select(Chapter).join(Note).where(Note.id == note_id)
        chapter: Chapter = self.db.execute(stmt).scalar_one()

        return chapter
