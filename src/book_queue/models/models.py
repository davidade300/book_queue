from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

# TODO: update  de class diagram to include id and title for notes,check relationships
reg = registry()


@reg.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, hash=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    edition: Mapped[int] = mapped_column(Integer)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher: Mapped[str] = mapped_column(
        String(255), nullable=False, hash=True
    )
    isbn: Mapped[int] = mapped_column(
        Integer, nullable=False, hash=True, unique=True
    )
    cover_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    chapters: Mapped[list['Chapter']] = relationship(
        back_populates='book',
        default_factory=list,
        cascade='all, delete-orphan',
    )


@reg.mapped_as_dataclass
class Chapter:
    __tablename__ = 'chapters'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False, hash=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, hash=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id'), nullable=False, init=False
    )
    book: Mapped[Book] = relationship(back_populates='chapters', init=False)
    notes: Mapped[list['Note']] = relationship(
        back_populates='chapter',
        default_factory=list,
        cascade='all, delete-orphan',
    )


@reg.mapped_as_dataclass
class Note:
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False, hash=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, hash=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey('chapters.id'), nullable=False, init=False
    )
    chapter: Mapped[Book] = relationship(Book, back_populates='notes')
