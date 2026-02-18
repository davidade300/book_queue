from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from book_queue.core.dependencies import get_db
from book_queue.core.schemas import (
    CreateNoteRequest,
    NoteResponse,
    NoteResponseList,
    UpdateNoteRequest,
)
from book_queue.models.models import Note
from book_queue.services.notes_service import NoteService

router = APIRouter(prefix='/notes', tags=['notes'])


@router.post(
    '/', response_model=NoteResponse, status_code=status.HTTP_201_CREATED
)
def create_note(
    request: CreateNoteRequest, db: Session = Depends(get_db)
) -> NoteResponse:
    note_service: NoteService = NoteService(db)
    note: Note = note_service.create(request)

    return NoteResponse.model_validate(note)


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db_session: Session = Depends(get_db)) -> None:
    note_service: NoteService = NoteService(db_session)
    note_service.delete(note_id)


@router.get(
    '/{note_id}', response_model=NoteResponse, status_code=status.HTTP_200_OK
)
def get_note_by_id(
    note_id: int, db_session: Session = Depends(get_db)
) -> NoteResponse:
    note_service: NoteService = NoteService(db_session)
    note: Note = note_service.get_by_id(note_id)

    return NoteResponse.model_validate(note)


@router.get('/by_book/{book_id}')
def get_notes_by_book_id(
    book_id: int, db_session: Session = Depends(get_db)
) -> NoteResponseList:
    note_service: NoteService = NoteService(db_session)
    note_list: list[NoteResponse] = [
        NoteResponse.model_validate(note)
        for note in note_service.list_by_book_id(book_id)
    ]

    result: NoteResponseList = NoteResponseList(notes=note_list)
    return result


@router.get(
    '/by_chapter/{chapter_id}',
    response_model=NoteResponseList,
    status_code=status.HTTP_200_OK,
)
def get_notes_by_chapter_id(
    chapter_id: int, db_session: Session = Depends(get_db)
) -> NoteResponseList:
    note_service: NoteService = NoteService(db_session)
    note_list: list[NoteResponse] = [
        NoteResponse.model_validate(note)
        for note in note_service.list_by_book_id(chapter_id)
    ]

    result: NoteResponseList = NoteResponseList(notes=note_list)
    return result


@router.patch(
    '/{note_id}', response_model=NoteResponse, status_code=status.HTTP_200_OK
)
def update_note(
    note_id: int,
    request: UpdateNoteRequest,
    db_session: Session = Depends(get_db),
):
    note_service: NoteService = NoteService(db_session)
    note: Note = note_service.update(note_id, request)

    return NoteResponse.model_validate(note)
