from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    edition: Mapped[int] = mapped_column(Integer)
    release_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    publisher: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    isbn_10: Mapped[str] = mapped_column(String(255), unique=True)
    isbn_13: Mapped[str] = mapped_column(String(255), unique=True)
    cover_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    chapters: Mapped[list['Chapter']] = relationship(
        back_populates='book',
        cascade='all, delete-orphan',
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )


class Chapter(Base):
    __tablename__ = 'chapters'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    summary: Mapped[str] = mapped_column(
        Text, default='Not finished/ não finalizado'
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id'),
        nullable=False,
    )
    book: Mapped[Book] = relationship(back_populates='chapters')
    notes: Mapped[list['Note']] = relationship(
        back_populates='chapter',
        cascade='all, delete-orphan',
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey('chapters.id'),
        nullable=False,
    )
    chapter: Mapped[Chapter] = relationship(back_populates='notes')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now()
    )
