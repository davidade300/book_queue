from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core.dependencies import get_db
from book_queue.core.schemas import (
    ChapterResponse,
    ChapterResponseList,
    CreateChapterRequest,
    UpdateChapterRequest,
)
from book_queue.models.models import Chapter
from book_queue.services.chapter_service import ChapterService

router = APIRouter(prefix='/chapters', tags=['chapters'])


@router.post(
    '/', response_model=ChapterResponse, status_code=status.HTTP_201_CREATED
)
def create_chapter(
    request: CreateChapterRequest, db: Session = Depends(get_db)
) -> ChapterResponse:
    chapter_service: ChapterService = ChapterService(db)
    chapter: Chapter = chapter_service.create(request)

    return ChapterResponse.model_validate(chapter)


@router.get(
    '/{chapter_id}',
    response_model=ChapterResponse,
    status_code=status.HTTP_200_OK,
)
def get_chapter_by_id(
    chapter_id: int, db: Session = Depends(get_db)
) -> ChapterResponse:
    chapter_service: ChapterService = ChapterService(db)
    chapter: Chapter = chapter_service.get_by_id(chapter_id)

    return ChapterResponse.model_validate(chapter)


@router.get(
    '/by_note/{note_id}',
    response_model=ChapterResponse,
    status_code=status.HTTP_200_OK,
)
def get_by_note_id(
    note_id: int, db: Session = Depends(get_db)
) -> ChapterResponse:
    chapter_service: ChapterService = ChapterService(db)
    chapter: Chapter = chapter_service.get_by_note_id(note_id)

    return ChapterResponse.model_validate(chapter)


@router.get(
    '/by_book/{book_id}',
    response_model=ChapterResponseList,
    status_code=status.HTTP_200_OK,
)
def list_chapters_by_book_id(
    book_id: int, db: Session = Depends(get_db)
) -> ChapterResponseList:
    chapter_service: ChapterService = ChapterService(db)
    chapter_list: list[ChapterResponse] = [
        ChapterResponse.model_validate(chapter)
        for chapter in chapter_service.list_by_book_id(book_id)
    ]

    result: ChapterResponseList = ChapterResponseList(chapters=chapter_list)

    return result


@router.get(
    '/list/', response_model=ChapterResponseList, status_code=status.HTTP_200_OK
)
def list_chapters(db: Session = Depends(get_db)) -> ChapterResponseList:
    chapter_service: ChapterService = ChapterService(db)
    chapter_list: list[ChapterResponse] = [
        ChapterResponse.model_validate(chapter)
        for chapter in chapter_service.list_chapters()
    ]

    result: ChapterResponseList = ChapterResponseList(chapters=chapter_list)

    return result


@router.delete('/{chapter_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)) -> None:
    chapter_service: ChapterService = ChapterService(db)
    chapter_service.delete(chapter_id)


@router.patch('/{chapter_id}', status_code=status.HTTP_200_OK)
def update_chapter(
    chapter_id: int,
    request: UpdateChapterRequest,
    db: Session = Depends(get_db),
) -> ChapterResponse:
    chapter_service: ChapterService = ChapterService(db)
    chapter: Chapter = chapter_service.update(chapter_id, request)

    return ChapterResponse.model_validate(chapter)
